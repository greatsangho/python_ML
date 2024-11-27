from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA


def load_file_and_split(file_path, chunk_size=1000, chunk_overlap=200):
    loader = PyPDFLoader(file_path)
    pages = loader.load()

    documents = [
        Document(page_content=page.page_content, metadata=page.metadata) for page in pages
    ]

    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " ", ""],
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    
    chunks = text_splitter.split_documents(documents)
    return chunks

def create_vector_store(vectorstore_name, chunks):
    embedding_model = OpenAIEmbeddings()
    texts = [chunk.page_content for chunk in chunks]
    metadatas = [{'chunk_index': i} for i in range(len(chunks))]
    ids = [f'chunk_{i}' for i in range(len(chunks))]

    vector_store = Chroma.from_texts(
        texts, 
        embedding=embedding_model, 
        metadatas=metadatas, 
        ids=ids, 
        persist_directory='./chroma_db'
    )
    vector_store.persist()
    return vector_store

def rag_chain(vector_store):
    retriever = vector_store.as_retriever(search_type='similarity', search_kwargs={'k': 3})
    llm = ChatOpenAI(model_name='gpt-4o-mini')
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return qa_chain
