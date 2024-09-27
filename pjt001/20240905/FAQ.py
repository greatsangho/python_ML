import pymysql
import pandas as pd

# 데이터베이스 연결 설정
def get_db_connection():
    conn = pymysql.connect(
        host='localhost',       # 데이터베이스 호스트
        user='root',    # 데이터베이스 사용자 이름
        password='1234',# 데이터베이스 비밀번호
        database='mydatabase'   # 사용할 데이터베이스 이름
    )
    return conn

# 데이터 읽기 (Read)
# 데이터 읽기 (Read) - 문자열로 반환
def get_faq_data(search_query=None):
    connection = pymysql.connect(
        host='localhost',  # 호스트 주소
        user='root',  # 사용자명
        password='1234',  # 비밀번호
        database='mydatabase',  # 데이터베이스명
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    try:
        with connection.cursor() as cursor:
            # 검색어가 있으면 WHERE 절에 LIKE 조건 추가
            if search_query:
                sql = "SELECT * FROM qna WHERE question LIKE %s OR answer LIKE %s"
                like_query = f"%{search_query}%"
                cursor.execute(sql, (like_query, like_query))
            else:
                sql = "SELECT * FROM qna "
                cursor.execute(sql)
            
            result = cursor.fetchall()
        return result
    finally:
        connection.close()

# 데이터 생성 (Create)
def create_data(content):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = 'INSERT INTO qna(answer) VALUES (%s)'
    cursor.execute(query, (content))
    conn.commit()
    conn.close()