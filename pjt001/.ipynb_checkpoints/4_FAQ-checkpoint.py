import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from FAQ import get_faq_data, get_categories
from matplotlib import font_manager
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

plt.rcParams['font.family'] ='Malgun Gothic'

def load_data():
    return pd.read_csv('car_data.csv')

car_data = load_data()


# 사이드바 메뉴
with st.sidebar:
    st.header("Menu")
    option = st.radio("Choose a section", ["데이터 조회", "FAQ"])

# 메인 콘텐츠 영역
st.markdown(
    """
    <style>
    .section-title {
        color: #4CAF50;
        font-size: 24px;
        margin-top: 20px;
    }
    .section-content {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True
)

if option == "데이터 조회":
    st.markdown('<div class="section-title">데이터 조회</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-content">조회할 데이터를 선택하세요</div>', unsafe_allow_html=True)

    data_option = st.radio("Select Data to View", ["연도별 차량 등록현황", "차종 등록비율-연도별"])

    if data_option == "연도별 차량 등록현황":
        st.subheader('연도별 차량 등록현황')
        fig, ax = plt.subplots(figsize=(10, 6))

        ax.bar(car_data['year'], car_data['승용'], label='승용', color='skyblue')
        ax.bar(car_data['year'], car_data['승합'], bottom=car_data['승용'], label='승합', color='orange')
        ax.bar(car_data['year'], car_data['화물'], bottom=car_data['승용'] + car_data['승합'], label='화물', color='green')
        ax.bar(car_data['year'], car_data['특수'], bottom=car_data['승용'] + car_data['승합'] + car_data['화물'], label='특수', color='red')

        ax.set_xlabel('Year')
        ax.set_ylabel('Quantity')
        ax.set_title('연도별 차량 등록현황')
        ax.set_xticks(car_data['year'])
        ax.set_xticklabels(car_data['year'])
        
        ax.legend()

        buf = BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        st.image(buf, use_column_width=True)
        buf.close()
        plt.close()

    elif data_option == "차종 등록비율-연도별":
        st.subheader('차종별 등록비율')
        selected_year = st.selectbox("Select a year for Pie Chart:", car_data['year'])
        
        if st.button('조회하기'):
            st.subheader(f'{selected_year}년 차종별 등록비율')
            
            car_types = car_data[car_data['year'] == selected_year].drop('year', axis=1).values.flatten()

            fig, ax = plt.subplots(figsize=(8, 8))
            ax.pie(car_types, labels=['승용', '승합', '화물', '특수'], autopct='%1.1f%%', startangle=90, colors=['skyblue', 'orange', 'green', 'red'])
            ax.set_title(f'{selected_year}년 차종 등록비율')

            buf = BytesIO()
            plt.savefig(buf, format="png")
            buf.seek(0)
            st.image(buf, use_column_width=True)
            buf.close()
            plt.close()

elif option == "FAQ":
    st.markdown('<div class="section-title">FAQ</div>', unsafe_allow_html=True)

    # 테이블 선택
    table_options = {
        '신고/문의 관련': 'qna',
        '자동차 생애주기별': 'qna2'
    }
    selected_table = st.selectbox("Select a table:", list(table_options.keys()))
    table_name = table_options[selected_table]

    # 테이블에서 카테고리 목록 가져오기
    categories = get_categories(table_name)
    selected_category = st.selectbox("Select a category:", ["All"] + categories)

    # 검색 입력란 추가
    search_query = st.text_input("Search FAQ")

    # 검색어와 카테고리 필터링
    faq_data = get_faq_data(table_name, category=selected_category if selected_category != "All" else None, search_query=search_query)

    # FAQ 데이터 표시
    if faq_data:
        for item in faq_data:
            with st.expander(f'{item["category"]}-{item["question"]}'):
                st.write(item['answer'])
    else:
        st.write("No results found for your search.")


