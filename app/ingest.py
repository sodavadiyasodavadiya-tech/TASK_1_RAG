import numpy as np
from app.embedder import embed_text
from app.database import get_db

def semantic_chunk(text, max_tokens=150):
    sentences = text.split(".")
    chunks = []
    current = ""

    for sentence in sentences:
        if len(current.split()) < max_tokens:
            current += sentence + "."
        else:
            chunks.append(current.strip())
            current = sentence + "."

    if current:
        chunks.append(current.strip())

    return chunks

def ingest_document(filename: str, text: str):
    chunks = semantic_chunk(text)
    conn = get_db()
    cur = conn.cursor()

    for idx, chunk in enumerate(chunks):
        embedding = embed_text(chunk)
        cur.execute("""
            INSERT INTO chunks (document, chunk_id, text, embedding)
            VALUES (?, ?, ?, ?)
        """, (
            filename,
            idx,
            chunk,
            embedding.tobytes()
        ))

    conn.commit()
    conn.close()
