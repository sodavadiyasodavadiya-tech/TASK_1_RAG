from fastapi import FastAPI, UploadFile, File, Query
from app.database import create_tables
from app.ingest import ingest_document
from app.retriever import retrieve_chunks
from app.qa import ask_llm

app = FastAPI(title="RAG Internship Task API")


@app.on_event("startup")
def startup_event():
    create_tables()


@app.get("/health")
def health():
    """
    Health check endpoint.
    Helps instantly identify if API is running.
    """
    return {
        "status": "ok",
        "message": "RAG system is running as expected"
    }


@app.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    """
    Upload and ingest a .txt document
    """
    if not file.filename.endswith(".txt"):
        return {
            "status": "error",
            "message": "Only .txt files are supported"
        }

    text = (await file.read()).decode("utf-8")
    ingest_document(file.filename, text)

    return {
        "status": "success",
        "message": f"{file.filename} ingested successfully"
    }


@app.post("/ask")
def ask(question: str = Query(..., min_length=3)):
    """
    Ask a question over ingested documents
    """
    retrieved = retrieve_chunks(question, top_k=3)

   
    if not retrieved:
        return {
            "question": question,
            "answer": "I don’t know based on the provided context",
            "confidence": 0.0,
            "evidence": []
        }

    context = "\n".join([item[1]["text"] for item in retrieved])

    answer = ask_llm(context, question)


    if answer.strip().lower().startswith("i don't know"):
        answer = retrieved[0][1]["text"]


    
    confidence = sum([item[0] for item in retrieved]) / len(retrieved)

    evidence = [
        {
            "document": item[1]["document"],
            "chunk_id": item[1]["chunk_id"],
            "text": item[1]["text"]
        }
        for item in retrieved
    ]

    return {
        "question": question,
        "answer": answer,
        "confidence": round(float(confidence), 2),
        "evidence": evidence
    }
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
