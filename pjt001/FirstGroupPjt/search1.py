import streamlit as st
import pandas as pd
import pymysql

# 데이터베이스에서 year와 kind 값을 가져오는 함수
def get_years_and_kinds(username='root', password='1234', host='localhost'):
    database_name = "carfirst"  # 고정된 데이터베이스 이름
    connection = pymysql.connect(
        host=host,
        user=username,
        password=password,
        database=database_name,
        cursorclass=pymysql.cursors.DictCursor
    )
    
    # 연도 데이터 가져오기
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT year FROM year")
        years = cursor.fetchall()
        year_list = [row['year'] for row in years]
    
    # 종류 데이터 가져오기
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT kind FROM kind")
        kinds = cursor.fetchall()
        kind_list = [row['kind'] for row in kinds]
    
    connection.close()
    
    return year_list, kind_list

# 검색 함수 정의
def search(year, kind, username='root', password='1234', host='localhost'):
    database_name = "carfirst"  # 고정된 데이터베이스 이름
    connection = pymysql.connect(
        host=host,
        user=username,
        password=password,
        database=database_name,
        cursorclass=pymysql.cursors.DictCursor
    )
    
    query = """
    SELECT y.year, k.kind, s.total 
    FROM year_kind_sum s 
    INNER JOIN year y ON s.year_id = y.year_id
    INNER JOIN kind k ON s.kind_id = k.kind_id
    WHERE (%s = 'All' OR y.year = %s)
    AND (%s = 'All' OR k.kind = %s)
    """
    
    with connection.cursor() as cursor:
        cursor.execute(query, (year, year, kind, kind))
        result = cursor.fetchall()

    connection.close()

    # DataFrame으로 변환
    result_df = pd.DataFrame(result, columns=['year', 'kind', 'total'])

    return result_df

# Streamlit UI
st.title("Data Search App")

# year와 kind 데이터를 불러와서 선택 옵션으로 제공
year_list, kind_list = get_years_and_kinds()

# "All" 옵션을 추가
year_list = ["All"] + year_list
kind_list = ["All"] + kind_list

# 사용자가 선택할 수 있는 선택 박스
year = st.selectbox("Select Year:", year_list)
kind = st.selectbox("Select Kind:", kind_list)

# 버튼을 눌렀을 때 검색 실행
if st.button("Search"):
    # 검색 함수 실행 및 결과 표시
    result = search(year, kind)
    
    if not result.empty:
        st.write("Search Results:")
        st.dataframe(result)  # 결과를 테이블 형태로 출력
    else:
        st.write("No results found.")
