from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.output_parsers import StrOutputParser
import os

# Assume GROQ_API_KEY is set as an environment variable
# os.environ["GROQ_API_KEY"] = "your_api_key_here" # For testing purposes

def load_vector_store():
    """Loads the FAISS vector store from the file."""
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = FAISS.load_local("../faiss_index", embeddings, allow_dangerous_deserialization=True)
    print("Loaded FAISS vector store from faiss_index.")
    return vector_store

def create_rag_chain(vector_store):
    """Creates a RAG chain for question answering."""
    retriever = vector_store.as_retriever()

    # Contextualize question prompt
    contextualize_q_system_prompt = """Given a chat history and the latest user question \
    which might reference context in the chat history, formulate a standalone question \
    which can be understood without the chat history. Do NOT answer the question, \
    just reformulate it if needed and otherwise return it as is."""
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            ("human", "{question}"),
        ]
    )
    llm = ChatGroq(temperature=0, model_name="mixtral-8x7b-32768")
    
    # Chain to contextualize the question
    contextualize_q_chain = contextualize_q_prompt | llm | StrOutputParser()

    # QA prompt
    qa_system_prompt = """You are an assistant for question-answering tasks. \
    Use the following pieces of retrieved context to answer the question. \
    If you don't know the answer, just say that you don't know. \
    Use three sentences maximum and keep the answer concise.\

    {context}"""
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt),
            ("human", "{question}"),
        ]
    )

    def contextualized_question(input: dict):
        if input.get("chat_history"):
            return contextualize_q_chain
        else:
            return input["question"]

    # RAG chain
    rag_chain = (
        RunnablePassthrough.assign(
            context=contextualized_question | retriever
        )
        | qa_prompt
        | llm
        | StrOutputParser()
    )
    
    print("Created RAG chain.")
    return rag_chain

if __name__ == "__main__":
    vector_store = load_vector_store()
    rag_chain = create_rag_chain(vector_store)
    
    # Example usage:
    # Ensure GROQ_API_KEY environment variable is set
    # if "GROQ_API_KEY" not in os.environ:
    #     print("GROQ_API_KEY environment variable not set. Please set it to run the RAG chain.")
    # else:
    #     question = "What is the introduction about?"
    #     response = rag_chain.invoke(question)
    #     print(f"Question: {question}")
    #     print(f"Answer: {response}")