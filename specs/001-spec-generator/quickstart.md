# Quickstart Guide

This guide provides instructions for setting up the local development environment for the book platform.

## Prerequisites

- **Node.js**: Version 20.x or higher
- **Python**: Version 3.11.x or higher
- **Git**: Ensure Git is installed on your system.

## 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

## 2. Backend Setup (API)

Navigate to the `api` directory and set up a virtual environment.

```bash
# Go to the API directory
cd api

# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt 
# Note: requirements.txt will be created in a later step. 
# For now, it would include 'fastapi', 'uvicorn', 'langchain', 'faiss-cpu'.
```

## 3. Frontend Setup (Book)

Navigate to the `book` directory.

```bash
# Go to the book directory
cd book

# Install dependencies
npm install
```

## 4. Running the Development Servers

You will need two separate terminals to run the backend and frontend servers simultaneously.

### Terminal 1: Run the Backend API

```bash
# Inside the 'api' directory with virtual env activated
uvicorn app.main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

### Terminal 2: Run the Frontend Book Site

```bash
# Inside the 'book' directory
npm start
```
The book website will be available at `http://localhost:3000`.

## 5. Content Processing

To generate the vector embeddings from the book content, you will run the processing script. This step is required whenever the content in `book/docs` is updated.

```bash
# Inside the root directory with the API's virtual env activated
python scripts/process_content.py
```
This will create or update the `faiss_index.bin` file used by the API.
