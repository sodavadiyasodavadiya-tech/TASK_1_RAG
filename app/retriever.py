import numpy as np
from app.database import get_db
from app.embedder import embed_text

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def retrieve_chunks(question, top_k=3):
    q_emb = embed_text(question)
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM chunks")
    rows = cur.fetchall()

    scored = []

    for row in rows:
        emb = np.frombuffer(row["embedding"], dtype="float32")
        score = cosine_similarity(q_emb, emb)
        scored.append((score, row))

    scored.sort(reverse=True, key=lambda x: x[0])

    top_chunks = scored[:top_k]
    conn.close()

    return top_chunks
