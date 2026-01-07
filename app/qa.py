import requests
import os
HF_API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"
HF_HEADERS = {
    "Authorization": f"Bearer {os.environ.get('HF_TOKEN')}"
}

def ask_llm(context: str, question: str) -> str:
    prompt = f"""
You are a strict question-answering system.

Rules:
- Answer ONLY using the provided context.
- If the answer IS present in the context, answer clearly and concisely.
- If the answer is NOT present, say exactly:
  "I don't know based on the provided context."

Context:
{context}

Question:
{question}

Answer:
"""

    response = requests.post(
        HF_API_URL,
        headers=HF_HEADERS,
        json={"inputs": prompt}

    )

    data = response.json()

    # HuggingFace response format
    if isinstance(data, list) and "generated_text" in data[0]:
        return data[0]["generated_text"].strip()

    return "I don't know based on the provided context."


