import requests

HF_API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"
HF_HEADERS = {
    "Authorization": "Bearer YOUR_HF_API_TOKEN"
}

def ask_llm(context: str, question: str) -> str:
    prompt = f"""
Answer ONLY using the context below.
If the answer is not present, say:
"I don't know based on the provided context."

Context:
{context}

Question:
{question}
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


