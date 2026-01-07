import requests

def ask_llm(context, question):
    prompt = f"""
You must answer ONLY using the context below.
If the answer is not present, say:
"I don’t know based on the provided context"

Context:
{context}

Question:
{question}
"""

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": "Bearer YOUR_API_KEY",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}]
        }
    )

    print(response.json())
    return "DEBUG"

