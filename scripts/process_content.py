from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

import os

def load_documents():
    """Loads documents from the book/docs directory."""
    script_dir = os.path.dirname(__file__)
    docs_path = os.path.abspath(os.path.join(script_dir, '..', 'book', 'docs'))
    loader = DirectoryLoader(docs_path, glob="**/*.mdx", show_progress=True)
    documents = loader.load()
    print(f"Loaded {len(documents)} documents.")
    return documents

def chunk_documents(documents):
    """Splits the documents into smaller chunks."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks.")
    return chunks

def create_vector_store(chunks):
    """Creates a FAISS vector store from the chunks."""
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = FAISS.from_documents(chunks, embeddings)
    print("Created FAISS vector store.")
    return vector_store

def save_vector_store(vector_store):
    """Saves the FAISS vector store to a file."""
    vector_store.save_local("../api/faiss_index")
    print("Saved FAISS vector store to api/faiss_index.")

if __name__ == "__main__":
    docs = load_documents()
    chunks = chunk_documents(docs)
    vector_store = create_vector_store(chunks)
    save_vector_store(vector_store)
