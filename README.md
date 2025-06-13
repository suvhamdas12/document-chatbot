![image](https://github.com/user-attachments/assets/2b05c7dd-e4fd-4fae-85e1-654512b9e9e5)![image](https://github.com/user-attachments/assets/2b05c7dd-e4fd-4fae-85e1-654512b9e9e5)
An intelligent document Q&A chatbot built with **FastAPI**, **React**, **LangChain**, **HuggingFace Embeddings**, and **Groq's LLMs**.
This app allows you to upload a PDF and ask questions, with answers derived strictly from the document using **Retrieval-Augmented Generation (RAG)**.

![Document ChatBot Screenshot](https://user-images.githubusercontent.com/placeholder/document-chatbot.png)

## 🔧 Features

- **📤 PDF Upload**: Upload PDF documents for analysis
- **📝 Text Extraction**: Extract text using PyMuPDF with OCR fallback (pytesseract)
- **🔍 Vector Search**: Store chunked documents as embeddings using HuggingFace + ChromaDB
- **💬 Natural Language Q&A**: Ask questions in plain English
- **🤖 Groq-Powered Responses**: Get accurate answers using **Groq's LLaMA 3-8B** model
- **🔄 Fallback Mechanism**: Intelligent fallback when vector search yields no results
- **💾 Persistent Storage**: ChromaDB for local vector storage

---

## 🚀 Tech Stack

### Frontend
- **React** + **Vite** for fast development
- **Axios** for API communication
- **Modern UI** with responsive design

### Backend
- **FastAPI** for high-performance API
- **LangChain** for RAG pipeline
- **Groq API** for LLM inference

### AI/ML Components
- **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2`
- **Vector Database**: ChromaDB (persistent local storage)
- **LLM**: `llama3-8b-8192` via Groq
- **OCR Fallback**: pdf2image + pytesseract

---

## 📁 Project Structure

```
document-chatbot/
│
├── backend/                    # FastAPI backend
│   ├── main.py                # Main FastAPI application
│   ├── requirements.txt       # Python dependencies
│   ├── uploaded_files/        # PDF storage directory
│   └── db/                    # ChromaDB persistence
│
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── App.jsx           # Main React component
│   │   ├── components/       # React components
│   │   └── styles/           # CSS styles
│   ├── public/               # Static assets
│   ├── package.json          # Node.js dependencies
│   └── vite.config.js        # Vite configuration
│
├── README.md                   # Project documentation
└── .gitignore                 # Git ignore rules
```

---

## 🛠️ Installation & Setup

### Prerequisites

- **Python 3.8+**
- **Node.js 16+**
- **Groq API Key** ([Get it here](https://console.groq.com/))

### 1️⃣ Backend Setup (FastAPI)

```bash
# Navigate to backend directory
cd backend/

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Alternative: Install dependencies manually
pip install fastapi uvicorn langchain langchain-groq langchain-community langchain-huggingface langchain-chroma pytesseract pdf2image pymupdf chromadb sentence-transformers
```

### 2️⃣ System Dependencies

```bash
# Install Tesseract OCR
# On macOS:
brew install tesseract

# On Ubuntu/Debian:
sudo apt-get install tesseract-ocr

# On Windows:
# Download from: https://github.com/UB-Mannheim/tesseract/wiki

# Install Poppler (required by pdf2image)
# On macOS:
brew install poppler

# On Ubuntu/Debian:
sudo apt-get install poppler-utils

# On Windows:
# Download from: https://blog.alivate.com.au/poppler-windows/
```

### 3️⃣ Environment Variables

Create a `.env` file in the backend directory:

```bash
# Backend/.env
GROQ_API_KEY=your_groq_api_key_here
```

Or set environment variable directly:

```bash
export GROQ_API_KEY="your_groq_api_key_here"
```

### 4️⃣ Frontend Setup (React)

```bash
# Navigate to frontend directory
cd frontend/

# Install Node.js dependencies
npm install

# Alternative: Using yarn
yarn install
```

---

## 🚀 Running the Application

### Start Backend Server

```bash
cd backend/
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`

### Start Frontend Development Server

```bash
cd frontend/
npm run dev
```

Frontend will be available at: `http://localhost:5173`

---

## 📖 Usage

1. **Upload PDF**: Click the upload button and select a PDF document
2. **Wait for Processing**: The app will extract text and create embeddings
3. **Ask Questions**: Type your question in the chat interface
4. **Get Answers**: Receive contextual answers based on your document

### Example Questions

- "What is the main topic of this document?"
- "Can you summarize the key points?"
- "What does the document say about [specific topic]?"

---

## 🔧 Configuration

### Backend Configuration

Edit `backend/main.py` to customize:

- **Chunk size**: Modify text splitting parameters
- **Embedding model**: Change HuggingFace model
- **LLM model**: Switch Groq model variant
- **Vector search**: Adjust similarity search parameters

### Frontend Configuration

Edit `frontend/src/App.jsx` to customize:

- **UI components**: Modify chat interface
- **API endpoints**: Update backend URLs
- **Styling**: Customize appearance

---

## 🧪 API Endpoints

### Backend API

- `POST /upload/`: Upload PDF document
- `POST /ask/`: Ask question about uploaded document
- `GET /health/`: Health check endpoint

### Example API Usage

```bash
# Upload PDF
curl -X POST "http://localhost:8000/upload/" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@document.pdf"

# Ask question
curl -X POST "http://localhost:8000/ask/" \
     -H "Content-Type: application/json" \
     -d '{"question": "What is this document about?"}'
```

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---


## 👥 Authors

- **Your Name** - *Initial work* - https://github.com/suvhamdas12

---

## 🙏 Acknowledgments

- **Groq** for providing fast LLM inference
- **LangChain** for RAG framework
- **ChromaDB** for vector storage
- **HuggingFace** for embeddings
- **FastAPI** for the backend framework
- **React** for the frontend framework


**⭐ Star this repository if you found it helpful!**
