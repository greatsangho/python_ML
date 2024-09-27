import streamlit as st
import pandas as pd
from FAQ import get_faq_data

# 카테고리와 질문을 묶어서 표시하기 위한 데이터 전처리
category_to_questions = {}
for category, question, answer in data:
    if category not in category_to_questions:
        category_to_questions[category] = []
    category_to_questions[category].append((question, answer))

# Streamlit 애플리케이션 시작
st.title("Q&A 리스트")

# 모든 질문과 답변을 확장 가능한 형태로 표시
for category, questions in category_to_questions.items():
    for question, answer in questions:
        expander_title = f"{category} - {question}"
        with st.expander(expander_title):
            st.write(answer)
