import streamlit as st
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

# 임베딩 및 데이터베이스 초기화
def initialize_vector_db():
    model_name = 'jhgan/ko-sroberta-multitask'
    embedding_model = HuggingFaceEmbeddings(model_name=model_name)
    persist_directory = 'path_insurance_db'
    vector_db = Chroma(persist_directory=persist_directory, embedding_function=embedding_model)
    return vector_db

# LLM 설정
def initialize_chain(vector_db):
    retriever = vector_db.as_retriever()
    llm = OpenAI(temperature=0.5)
    chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return chain

# 스트림릿 앱 시작
st.title("PDF 기반 QA 시스템")
st.markdown("보험 약관 및 문서에서 정보를 검색하세요.")

# 사용자가 질문 입력
query = st.text_input("질문을 입력하세요:", placeholder="예: 자동차 접촉 사고 시 어떤 보장을 받을 수 있어?")

# 데이터베이스 및 QA 체인 초기화
vector_db = initialize_vector_db()
chain = initialize_chain(vector_db)

# 질문 처리
if query:
    with st.spinner("답변을 생성 중입니다..."):
        try:
            answer = chain.run(query)
            st.success("답변을 생성했습니다!")
            st.markdown(f"### 질문: {query}")
            st.markdown(f"**답변:** {answer}")
        except Exception as e:
            st.error(f"오류 발생: {e}")

# 추가: 검색된 문서 메타데이터 출력 (선택 사항)
if st.checkbox("관련 문서 보기"):
    result = chain(query, return_metadata=True)
    st.markdown("### 관련 문서")
    for doc in result["source_documents"]:
        st.markdown(f"- **Page {doc.metadata['page']}:** {doc.page_content[:168]}...")

# 실행 명령
# 터미널에서 실행: `streamlit run app.py`