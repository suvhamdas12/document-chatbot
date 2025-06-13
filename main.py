import os
import shutil
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
import fitz  # PyMuPDF
from tempfile import TemporaryDirectory
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

app = FastAPI()

# Enable CORS (for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Or 3000 if using CRA
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Globals
VECTOR_DB_DIR = "db"
UPLOAD_DIR = "uploaded_files"

# Set your Groq API key (or load from .env)
os.environ["GROQ_API_KEY"] = "************"

# === Utility to extract text from a PDF using PyMuPDF ===
from pdf2image import convert_from_path
import pytesseract

def extract_text_from_pdf(pdf_path):
    try:
        text = ""
        with fitz.open(pdf_path) as doc:
            for page in doc:
                page_text = page.get_text()
                if page_text.strip():
                    text += page_text
        if text.strip():
            return text
    except:
        pass

    # Fallback to OCR
    print("Fallback to OCR extraction")
    pages = convert_from_path(pdf_path)
    text = ""
    for i, page in enumerate(pages):
        ocr_text = pytesseract.image_to_string(page)
        text += f"\n\nPage {i+1}:\n" + ocr_text
    print("Full extracted text:\n", text[:500])
    return text



# === Endpoint to upload a PDF and process it ===
@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        # Save the uploaded file
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Extract and split text
        full_text = extract_text_from_pdf(file_path)
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        docs = splitter.create_documents([full_text])

        # Generate embeddings using HuggingFace
        embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        # Store in Chroma
        vectordb = Chroma.from_documents(docs, embedding=embedding_function, persist_directory=VECTOR_DB_DIR)
        vectordb.persist()
        for i, doc in enumerate(docs):
            print(f"Embedding chunk {i+1}: {doc.page_content[:200]}")
        print(f"Extracted {len(docs)} chunks from PDF.")
        return {"message": "PDF processed and stored in vector DB"}

    except Exception as e:
        return {"error": str(e)}

# === Endpoint to ask questions ===
@app.get("/ask/")
async def ask_question(question: str):
    try:
        # Load vector store
        vectordb = Chroma(
            persist_directory=VECTOR_DB_DIR,
            embedding_function=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        )
        retriever = vectordb.as_retriever()
        docs = retriever.invoke(question)

        print(f"Top relevant docs for question '{question}':")
        for d in docs:
            print(d.page_content[:150])  # Preview

        if not docs:
            print("⚠️ No relevant docs retrieved — falling back to raw method.")
            # fallback to raw
            llm = ChatGroq(groq_api_key=os.environ["GROQ_API_KEY"], model_name="llama3-8b-8192")
            text = extract_text_from_pdf("uploaded_files/Suvham Das report .pdf")  # optional: make dynamic
            fallback_answer = llm.invoke(f"Based on the following document, answer: {question}\n\n{text}")
            return {"answer": fallback_answer.content}

        # Otherwise, run normal RAG
        llm = ChatGroq(groq_api_key=os.environ["GROQ_API_KEY"], model_name="llama3-8b-8192")
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            return_source_documents=True
        )

        result = qa_chain.invoke({"query": f"Answer based strictly on the uploaded document: {question}"})
        print("LLM result:", result["result"])
        return {"answer": result["result"]}

    except Exception as e:
        print("❌ Exception:", e)
        return {"error": str(e)}
    
@app.get("/ask_raw/")
async def ask_raw(question: str):
    llm = ChatGroq(groq_api_key=os.environ["GROQ_API_KEY"], model_name="llama3-8b-8192")
    text = extract_text_from_pdf("uploaded_files/Suvham Das report .pdf")
    return {"answer": llm.invoke(f"Based on the following document, answer: {question}\n\n{text}")}
