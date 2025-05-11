
from fastapi import FastAPI, UploadFile, File, HTTPException
import fitz  # PyMuPDF
import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json 
from transformers import pipeline
from pydantic import BaseModel
from datetime import datetime




app = FastAPI()

os.makedirs("data", exist_ok=True) 

for filename in os.listdir("data"):
    file_path = os.path.join("data", filename)
    
    # Check if it is a file (not a subdirectory)
    if os.path.isfile(file_path):
        os.remove(file_path)  # Remove the file
        print(f"Deleted file: {filename}")


DATA_PATH = "data/latest.txt"  # where you save the extracted text

with open("data/logs.txt", "w") as f:
        f.write(f"Date and Time,Question,Answer\n")

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        return "\n".join(page.get_text() for page in doc)

def save_text(text: str):
    os.makedirs("data", exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        f.write(text)

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    pdf_bytes = await file.read()
    text = extract_text_from_pdf(pdf_bytes)
    save_text(text)
    return {"message": "PDF processed and text saved."}  


def split_text(text, chunk_size=100, overlap=50):
    words = text.split()
    for i in range(0, len(words), chunk_size - overlap):
        yield " ".join(words[i:i + chunk_size])

def generate_embeddings():
    model = SentenceTransformer("all-MiniLM-L6-v2")

    text = open(DATA_PATH, "r")

    lines = " ".join(text.readlines())

    chunks = list(split_text(lines))

    with open("data/chunks.json", "w") as f:
        json.dump(chunks, f)

    embeddings = model.encode(chunks)


    return embeddings


def index_init():

    embeddings = generate_embeddings()
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))

    faiss.write_index(index, "data/index.faiss")

    return 


def retrieve(query, top_k=3):
    model = SentenceTransformer("all-MiniLM-L6-v2")

    index_init()

    index = faiss.read_index("data/index.faiss")

    with open("data/chunks.json", "r", encoding="utf-8") as f:
        chunks = json.load(f)

    q_emb = model.encode([query])
    D, I = index.search(np.array(q_emb), top_k)

    return [chunks[i] for i in I[0]]

def answer_question(question):
    qa = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")
    contexts = retrieve(question)
    best = {"score": 0, "answer": ""}

    for context in contexts:
        result = qa(question=question, context=context)
        if result["score"] > best["score"]:
            best = result

    return best

class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    answer = answer_question(request.question)

    with open("data/logs.txt", "a") as f:
        f.write(f"{datetime.now()},{request.question},{answer['answer']}\n")

    return answer["answer"]