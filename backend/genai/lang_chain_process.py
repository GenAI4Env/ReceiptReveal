import getpass
import os
from dotenv import load_dotenv
import google.generativeai as genai
# langchain libraries
from langchain.chains import RetrievalQA
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.vectorstores import DocArrayInMemorySearch
from langchain.schema.runnable import RunnableMap
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# --- loading env for api keys ---
load_dotenv()

# --- fetch the google gemini ---
llm = ChatGoogleGenerativeAI(model="gemini-2.0-pro-exp", temperature=0.7)
#result = llm.invoke("hello who is this?")
#print(result.text)

#  ------ setup RAG -----

loader = CSVLoader(file_path="./genai/Food_Production.csv")
data = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = text_splitter.split_documents(data)
embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
vectorstore = DocArrayInMemorySearch.from_documents(
        docs,
        embedding=embeddings
)

# making the RAG
retriever = vectorstore.as_retriever()
#print(retriever.get_relevant_documents("Who is the current CEO of microsoft?"))
# --- Making chain ---
# setting up the format for output and the specific prompt engineering 
template ="""You are a personal carbon footprint estimator expert.
Your answer should be based off this context: {context}
if the database does not have the answer, please provide your best estimate based on information you have found from the web.
Do not say I dont know.
Respond in numbers only, in the json format:
{{"answer": "...", "confidence": "..."}}
Where confidence is a value between 0 and 1, with 1 being completely confident and 0 being not confident at all.
for this question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
output_parser = StrOutputParser()
# creating chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",  # "stuff" is a simple chain type.  Explore others like "map_reduce"
    retriever=retriever,
    return_source_documents=False,  # Return the source documents used for context
     chain_type_kwargs={"prompt": prompt}
)

a = qa_chain({"query": "What is the carbon footprint of a egg?"})["result"]
print(a)