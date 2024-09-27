import streamlit as st
import matplotlib.pyplot as plt

# Streamlit 제목
st.title('연도별 데이터 파이차트')

# 사용자 입력 받기
st.sidebar.header('데이터 입력')
years = st.sidebar.text_input('연도 입력 (쉼표로 구분)', '2020, 2021, 2022, 2023')
values_input = st.sidebar.text_input('값 입력 (쉼표로 구분)', '30, 20, 25, 25')

# 입력된 데이터를 처리
try:
    years_list = [year.strip() for year in years.split(',')]
    values_list = [float(value.strip()) for value in values_input.split(',')]

    if len(years_list) != len(values_list):
        st.error('연도와 값의 개수가 일치하지 않습니다.')
    else:
        # 파이차트 그리기
        fig, ax = plt.subplots()
        ax.pie(values_list, labels=years_list, autopct='%1.1f%%', startangle=140)
        ax.set_aspect('equal')  # 원형 차트가 원형으로 보이도록 설정

        # Streamlit에 Matplotlib 차트 표시
        st.pyplot(fig)
except ValueError:
    st.error('값 입력에서 숫자가 아닌 항목이 포함되어 있습니다. 숫자만 입력해 주세요.')
