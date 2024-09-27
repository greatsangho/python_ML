import streamlit as st

# 데이터 정의
data = [
    ["기술", "파이썬이란 무엇인가요?", "파이썬은 고급 프로그래밍 언어로, 코드가 간결하고 읽기 쉽습니다."],
    ["기술", "딥러닝이란 무엇인가요?", "딥러닝은 인공신경망을 기반으로 한 기계 학습의 한 분야입니다."],
    ["역사", "한국전쟁은 언제 시작되었나요?", "한국전쟁은 1950년 6월 25일에 시작되었습니다."],
    ["역사", "로마 제국의 멸망 원인은 무엇인가요?", "로마 제국의 멸망 원인은 내부의 정치적 혼란과 외부의 침입 등이 복합적으로 작용했습니다."],
    ["과학", "빛의 속도는 얼마인가요?", "빛의 속도는 약 299,792,458 미터/초입니다."],
    ["과학", "지구의 평균 기온은 얼마인가요?", "지구의 평균 기온은 약 15도 섭씨입니다."]
]

# 카테고리와 질문을 묶어서 표시하기 위한 데이터 전처리
category_to_questions = {}
for category, question, answer in data:
    if category not in category_to_questions:
        category_to_questions[category] = []
    category_to_questions[category].append((question, answer))

# Streamlit 애플리케이션 시작
st.title("Q&A 검색")

# 검색 입력 받기
search_term = st.text_input("검색어를 입력하세요", "")

# 검색어로 필터링된 질문과 답변 표시
for category, questions in category_to_questions.items():
    for question, answer in questions:
        if search_term.lower() in question.lower() or search_term.lower() in answer.lower():
            expander_title = f"{category} - {question}"
            with st.expander(expander_title):
                st.write(answer)
