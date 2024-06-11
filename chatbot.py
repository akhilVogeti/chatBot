import streamlit as st
from PyPDF2 import PdfReader
from langchain.chains.question_answering import load_qa_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI


OPENAI_API_KEY = "sk-proj-OIykabzihn2SJr1eBB1nT3BlbkFJZQsXWXMyvMXOepLJxmPF"


def extract_text_from_pdf(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


def compute_embeddings(text):
    text_splitter = RecursiveCharacterTextSplitter(
        separators="\n",
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vector_store = FAISS.from_texts(chunks, embeddings)
    return vector_store


def main():
    st.header("Enter your text")
    user_input = st.text_area("Enter Text", height=100)

    with st.sidebar:
        st.title("Your documents")
        file = st.file_uploader("Upload a pdf file and start asking questions", type="pdf")

    text_pdf = ""
    if file:
        text_pdf = extract_text_from_pdf(file)

    text = user_input + text_pdf

    if text:
        st.header("Q & A")
        vector_store = compute_embeddings(text)
        user_question = st.text_input("Type your question")
        st.write(user_question)

        if user_question:
            match = vector_store.similarity_search(user_question)
            llm = ChatOpenAI(
                openai_api_key=OPENAI_API_KEY,
                temperature=0,
                max_tokens=1000,
                model_name="gpt-3.5-turbo"
            )
            chain = load_qa_chain(llm, chain_type="stuff")
            response = chain.run(input_documents=match, question=user_question)
            st.write(response)


if __name__ == "__main__":
    main()
