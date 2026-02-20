import ollama
from app.config import *

def generate_response(messages):
    response = ollama.chat(
        model=ai_model,
        messages=messages,
        options={"temperature": 0.3}
    )
    return response["message"]["content"]


def summarize_messages(messages, summary):
        
    text_block = f"system: {summary}\n" + "\n".join(
        [f"{m.role}: {m.content}" for m in messages]
    )

    response = ollama.chat(
        model=ai_model,
        messages=[
            {
                "role": "system",
                "content": "Summarize the conversation keeping key technical details."
            },
            {
                "role": "user",
                "content": text_block
            }
        ],
        options={"temperature": 0.2}
    )

    return response["message"]["content"]