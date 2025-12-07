from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from models import ChatRequest, ChatResponse
from services.rag_service import load_vector_store, create_rag_chain
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
import os

app = FastAPI()

@app.middleware("http")
async def log_requests_and_handle_errors(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    try:
        response = await call_next(request)
        logger.info(f"Response status code: {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "An internal server error occurred"},
        )

# Load vector store and create RAG chain globally
# This ensures it's loaded only once at startup
vector_store = load_vector_store()
rag_chain = create_rag_chain(vector_store)

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Handles chat requests, invoking the RAG chain to generate a response.
    """
    if "GROQ_API_KEY" not in os.environ:
        return ChatResponse(
            answer="GROQ_API_KEY environment variable not set. Please set it to run the RAG chain.",
            sources=[]
        )
    
    question = request.query
    chat_history = request.conversation_history

    response = rag_chain.invoke({"question": question, "chat_history": chat_history})
    
    # Extract sources from the context
    sources = []
    if "context" in response and hasattr(response["context"], "__iter__"):
        for doc in response["context"]:
            if hasattr(doc, "metadata") and "source" in doc.metadata:
                sources.append(doc.metadata["source"])
    
    return ChatResponse(answer=response['answer'], sources=sources)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
