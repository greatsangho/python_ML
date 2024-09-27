import streamlit as st
import pandas as pd
import numpy as np

# 제목과 설명 출력
st.title("Streamlit 데이터 시각화 예제")
st.write("이 앱은 사용자 입력에 따라 데이터를 동적으로 필터링하고 시각화합니다.")

# 데이터프레임 생성
np.random.seed(0)
data = {
    'A': np.random.randint(1, 100, 100),
    'B': np.random.randint(1, 100, 100),
    'C': np.random.randint(1, 100, 100),
    'D': np.random.choice(['X', 'Y', 'Z'], 100)
}
df = pd.DataFrame(data)

# 사용자 입력 받기: 숫자 슬라이더
min_value = st.slider('A 열의 최소값 선택', min_value=int(df['A'].min()), max_value=int(df['A'].max()), value=int(df['A'].min()))

# 사용자 입력 받기: 선택 상자
selected_category = st.selectbox('D 열의 카테고리 선택', df['D'].unique())

# 데이터 필터링
filtered_df = df[(df['A'] >= min_value) & (df['D'] == selected_category)]

# 필터링된 데이터프레임 출력
st.write("필터링된 데이터프레임:")
st.dataframe(filtered_df)

# 차트 시각화
st.write("B 열과 C 열의 산점도:")
st.scatter_chart(filtered_df[['B', 'C']])

# 통계 정보 출력
st.write("필터링된 데이터의 기본 통계:")
st.write(filtered_df.describe())
