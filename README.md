# Physical AI & Humanoid Robotics Book

This project is a book about Physical AI and Humanoid Robotics, built with Docusaurus. It includes a RAG-based chatbot that can answer questions about the book's content.

## Architecture

The project is divided into three main parts:

- **`book/`**: A Docusaurus website that serves the book's content.
- **`api/`**: A FastAPI backend that provides a RAG-based chat API.
- **`scripts/`**: A Python script to process the book's content into a FAISS index for the RAG model.

## Setup and Running

### Prerequisites

- Node.js (v16 or later)
- Python (v3.9 or later)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Install book dependencies:**
   ```bash
   cd book
   npm install
   ```

3. **Install API dependencies:**
   ```bash
   cd ../api
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the Docusaurus development server:**
   ```bash
   cd book
   npm start
   ```

2. **Start the FastAPI backend:**
   ```bash
   cd ../api
   uvicorn app.main:app --reload
   ```

The book will be available at `http://localhost:3000` and the API at `http://localhost:8000`.
