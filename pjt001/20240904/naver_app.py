import streamlit as st
import pandas as pd
from naver_news_connection import get_faq_data

st.title("FAQ")

# 검색 입력란 추가
search_query = st.text_input("Search FAQ")

# 검색어에 따른 FAQ 데이터 필터링
faq_data = get_faq_data(search_query)

# FAQ 데이터 표시
if faq_data:
    for item in faq_data:
        with st.expander(item['title']):
            st.write(item['content'])
else:
    st.write("No results found for your search.")
