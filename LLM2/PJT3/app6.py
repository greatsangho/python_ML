import tempfile
import numpy as np
import streamlit as st
from models import load_file_and_split, create_vector_store, rag_chain
from langchain.chat_models import ChatOpenAI
from sklearn.metrics.pairwise import cosine_similarity
from langchain.embeddings import OpenAIEmbeddings

import os
os.environ['OPENAI_API_KEY']='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'


def extract_question_intent_and_keywords(user_input):
    import re
    keywords = re.findall(r'\w+', user_input)
    intent = "정보 요청" if "알려줘" in user_input or "설명" in user_input else "기타"
    return {"keywords": keywords, "intent": intent}


def filter_retrieved_documents_with_intent(user_query, retrieved_texts):
    analysis = extract_question_intent_and_keywords(user_query)
    keywords = analysis["keywords"]
    filtered_texts = [
        text for text in retrieved_texts if any(keyword.lower() in text.lower() for keyword in keywords)
    ]
    return filtered_texts if filtered_texts else retrieved_texts


def evaluate_retrieval_consistency(retrieved_texts, model_response, user_query):
    """
    검색된 문서와 생성된 응답 간의 유사도를 계산합니다.
    """
    embedding_model = OpenAIEmbeddings()
    
    
    if not retrieved_texts:
        return None

    
    retrieved_embeddings = embedding_model.embed_documents(retrieved_texts)
    response_embedding = embedding_model.embed_query(model_response)
    query_embedding = embedding_model.embed_query(user_query)

    
    query_similarities = cosine_similarity([query_embedding], retrieved_embeddings).flatten()
    response_similarities = cosine_similarity([response_embedding], retrieved_embeddings).flatten()

    avg_query_similarity = np.mean(query_similarities) if query_similarities.size > 0 else 0
    max_response_similarity = max(response_similarities) if response_similarities.size > 0 else 0

    return (avg_query_similarity + max_response_similarity) / 2


def generate_intelligent_prompt(user_input, retrieved_texts, mode="basic"):
    """
    문서 내용과 질문을 기반으로 프롬프트를 생성합니다.
    """
    if mode == "basic":
        return f"질문: {user_input}\n운전자 보험 관련 답변을 제공하세요."

    elif mode == "engineered":
        if not retrieved_texts:
            return (
                f"문서에 관련된 정보가 없습니다. 질문에 대한 답변은 "
                f"'관련 문서가 없습니다'라고 제공해야 합니다."
            )
        context = "\n".join(retrieved_texts[:3])  # 상위 3개의 문서 텍스트
        return (
            f"아래는 운전자 보험과 관련된 문서입니다. 문서 내용을 반드시 기반으로 "
            f"답변을 생성하세요. 문서에 없는 내용에 대해 유추하지 마세요.\n\n"
            f"문서 내용:\n{context}\n\n"
            f"질문: {user_input}\n"
            f"답변:"
        )
    else:
        raise ValueError("Invalid mode. Choose 'basic' or 'engineered'.")


st.title("🗨️ 질의응답 시스템")
st.sidebar.title("설정")


if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None
if "history" not in st.session_state:
    st.session_state.history = []
if "default_model" not in st.session_state:
    st.session_state.default_model = ChatOpenAI(model_name="gpt-4")
if "processed_file" not in st.session_state:
    st.session_state.processed_file = ""
if "response_mode" not in st.session_state:
    st.session_state.response_mode = "basic"  
if "similarity_scores" not in st.session_state:
    st.session_state.similarity_scores = {"basic": None, "engineered": None}


uploaded_file = st.sidebar.file_uploader("PDF 파일 업로드", type=["pdf"])

if uploaded_file:
    if st.session_state.processed_file != uploaded_file.name:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(uploaded_file.read())
            temp_file_path = temp_file.name

        with st.spinner("파일 처리 중..."):
            chunks = load_file_and_split(temp_file_path)
            vector_store = create_vector_store(uploaded_file.name, chunks)
            st.session_state.qa_chain = rag_chain(vector_store)
            st.session_state.processed_file = uploaded_file.name
        st.sidebar.success(f"파일 `{uploaded_file.name}` 처리 완료!")
    else:
        st.sidebar.info(f"파일 `{uploaded_file.name}`은 이미 처리되었습니다.")


st.session_state.response_mode = st.sidebar.radio(
    "응답 모드 선택:",
    options=["basic", "engineered"],
    format_func=lambda x: "기본 프롬프트" if x == "basic" else "프롬프트 엔지니어링",
    horizontal=True
)


if st.session_state.history:
    for chat in st.session_state.history:
        with st.chat_message("user"):
            st.markdown(chat["user"])
        with st.chat_message("assistant"):
            if st.session_state.response_mode == "basic":
                st.markdown(chat["basic_answer"])
            else:
                st.markdown(chat["engineered_answer"])


def handle_user_input():
    user_input = st.session_state.get("dynamic_user_input", "").strip()
    if user_input:
        if st.session_state.qa_chain:
            with st.spinner("답변 생성 중..."):
                # 검색 및 필터링
                intent_analysis = extract_question_intent_and_keywords(user_input)
                preprocessed_query = " ".join(intent_analysis["keywords"])
                retrieved_docs = st.session_state.qa_chain.retriever.get_relevant_documents(preprocessed_query)
                retrieved_texts = [doc.page_content for doc in retrieved_docs]
                filtered_texts = filter_retrieved_documents_with_intent(user_input, retrieved_texts)


                basic_prompt = generate_intelligent_prompt(user_input, filtered_texts, mode="basic")
                basic_answer = st.session_state.qa_chain.run(basic_prompt)

                engineered_prompt = generate_intelligent_prompt(user_input, filtered_texts, mode="engineered")
                engineered_answer = st.session_state.qa_chain.run(engineered_prompt)

                
                basic_score = evaluate_retrieval_consistency(filtered_texts, basic_answer, user_input)
                engineered_score = evaluate_retrieval_consistency(filtered_texts, engineered_answer, user_input)

        
                st.session_state.similarity_scores = {
                    "basic": basic_score if basic_score is not None else 0.0,
                    "engineered": engineered_score if engineered_score is not None else 0.0,
                }

        else:
            with st.spinner("답변 생성 중..."):
                basic_answer = st.session_state.default_model.predict(f"질문: {user_input}\n운전자 보험 관련 답변을 제공하세요.")
                engineered_answer = "관련 문서가 없습니다."
                filtered_texts = []

            
                st.session_state.similarity_scores = {"basic": 0.0, "engineered": 0.0}

        st.session_state.history.append(
            {
                "user": user_input,
                "basic_answer": basic_answer,
                "engineered_answer": engineered_answer,
            }
        )
        st.session_state["dynamic_user_input"] = ""

st.text_input(
    "질문을 입력하세요:",
    value="",
    key="dynamic_user_input",
    placeholder="질문을 입력하고 Enter 키를 눌러주세요.",
    on_change=handle_user_input,
    label_visibility="collapsed",
)


if st.session_state.similarity_scores["basic"] is not None:
    st.sidebar.write(f"🔍 Basic Prompt Score: {st.session_state.similarity_scores['basic']:.4f}")
if st.session_state.similarity_scores["engineered"] is not None:
    st.sidebar.write(f"🔍 Engineered Prompt Score: {st.session_state.similarity_scores['engineered']:.4f}")


if st.sidebar.button("대화 초기화"):
    st.session_state.history = []
    st.session_state.response_mode = "basic"
    st.rerun()
