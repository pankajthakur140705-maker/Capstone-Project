from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_llm(message: str):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are Bandhu AI, a helpful government scheme assistant."},
            {"role": "user", "content": message}
        ]
    )

    return response.choices[0].message.content