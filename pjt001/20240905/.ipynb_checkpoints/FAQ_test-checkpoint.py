import streamlit as st
import pandas as pd
from FAQ import get_faq_data

# Streamlit 애플리케이션 시작
st.title("Q&A 드롭다운")

# 카테고리 추출
categories = list(set(item[0] for item in data))

# 카테고리 선택
selected_category = st.selectbox("카테고리를 선택하세요", categories)

# 선택된 카테고리의 질문 리스트 가져오기
questions_for_category = [item[1] for item in data if item[0] == selected_category]

# 질문 선택
selected_question = st.selectbox("질문을 선택하세요", questions_for_category)

# 선택된 질문에 대한 답변 찾기
answer = next(item[2] for item in data if item[1] == selected_question)

# 답변 표시
st.write("답변: ", answer)
