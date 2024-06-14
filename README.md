# AI-powered Q&A 

A python application that uses ChatGPT and langchain to respond to your questions/prompts on an uploaded pdf or text input.

## Requirements
1. OpenAI API Key (paid)
2. Required Packages:  

    - streamlit: A Python library for creating interactive web applications.
    - PyPDF2: A library for working with PDF files in Python.
    - langchain: A library for building question-answering systems.
    - langchain_openai: An extension for langchain that integrates OpenAI's API.
    - langchain_community.vectorstores: A subpackage within langchain that provides tools for vector stores.
    - openai: The official OpenAI API client library (may be included with langchain_openai).

## How to run
1. clone the repo.
````
git clone https://github.com/akhilVogeti/chatBot.git 
````
2. Move to the root directory
````
cd chatBot
````
3. Install the dependencies 
````
pip install streamlit PyPDF2 langchain langchain_openai langchain_community
````
Any missing dependencies will be mentioned in the error message. Do install them using pip install command.
4. Run the code
````
streamlit run chatbot.py
````
5. Browser automatically opens. After a pdf is uploaded or input text is given or both, you can ask questions in the Q&A section. Until a pdf is uploaded or input text given, the Q&A box wont appear. 

## Output 
Here are some screenshots of the output

![screenshot1.jpg](screenshot1.jpg)
Screenshot showing convo summerisation.




![Screenshot2.jpg](Screenshot2.jpg)
Screenshot showing that AI doesnt know the info from the pdf alone.




![screenshot3.jpg](screenshot3.jpg)
It now answers the question based on pdf + text input.




![screenshot4.png](screenshot4.png)
Answers questions based on pdf content alone.



## How this works
1. Text Processing <br>
    * Accepts text input, PDFs, or both. <br>
    * Extracts text from text input, PDFs, or both. <br>
    * Divides extracted text into smaller chunks. <br>

2. Embedding Generation <br>
    * Computes embeddings for each text chunk (capturing meaning). <br>

3. Role of FAISS <br>
    * FAISS (Facebook AI Similarity Search) library is used forfor similatiry search. The text chunks most similar to the user's question are found using similarity             search. They are called matches in the code. <br>
    * FAISS.from_texts is used to create a FAISS index (vector_store) from these text chunks and their corresponding embeddings. <br>
      
4. Question Answering with GPT-3.5-turbo <br>
    * Leverages load_qa_chain function from Langchain with GPT-3.5-turbo as the llm . <br>
    * Uses the "stuff" document chain_type for simplicity. <br>
    * The chain.run combines (or "stuffs")  user question and retrieved matches (similar chunks) into a prompt and a response is generated. <br>
  
