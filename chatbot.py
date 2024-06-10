import streamlit as st
from PyPDF2 import PdfReader
from langchain.chains.question_answering import load_qa_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI


OPENAI_API_KEY = "sk-proj-OIykabzihn2SJr1eBB1nT3BlbkFJZQsXWXMyvMXOepLJxmPF"


st.header("Q & A")

with st.sidebar:
    st.title("Your documents")
    file = st.file_uploader("Upload a pdf file and start asking questions", type="pdf")


if file is not None:
    pdf_reader = PdfReader(file)
    text = ""

    for page in pdf_reader.pages:
        text = text+page.extract_text()

    text_splitter = RecursiveCharacterTextSplitter(
        separators="\n",
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len
    )
    chunks = text_splitter.split_text(text)

    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY )

    vector_store = FAISS.from_texts(chunks,embeddings)

    user_question = st.text_input("Type your question")

    #similarity search
    if user_question:
        match = vector_store.similarity_search(user_question)
        llm = ChatOpenAI(
            openai_api_key=OPENAI_API_KEY,
            temperature=0,
            max_tokens=1000,
            model_name="gpt-3.5-turbo"
        )
        # chain -> take the question, get relevant document, pass it to the LLM, generate the output
        chain = load_qa_chain(llm, chain_type="stuff")
        response = chain.run(input_documents=match, question=user_question)
        st.write(response)




