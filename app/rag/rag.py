import ollama
from flask import current_app


def generate_answer(question):

    rag = current_app.app_rag 
    results = rag.retrieve(question)

    context_chunks  = []
    sources = set()

    for item in results:
        context_chunks.append(item["text"])
        sources.add(item["metadata"]["source"])
    
    context = "\n\n".join(context_chunks)
    
    # if len(context) > 3000:
    #     context = context[:3000]

    response = ollama.chat(
        model="gemma3:1b",
        messages=[
            {
                "role": "system",
                "content":  
                """
                You are an assistant answering questions based strictly on provided context.
                If the answer is not in the context, say:
                "I cannot find the answer in the document."
                Be clear and structured.
                """
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}"
            }
        ],
        options={"temperature": 0.2}
    )

    answer = response["message"]["content"]

    return {
        "answer": answer,
        "sources": list(sources)
    }

# rag = RAGService(r"./static/pdf/ICS2_mod2.1.pdf")

# answer = generate_answer("Что такое межсетевой экран? ответ на русском")

# print("\nANSWER:\n")
# print(answer)
