from flask import Blueprint, request, jsonify
from app.rag.rag import generate_answer


ask_pdf = Blueprint("ask_pdf", __name__)

@ask_pdf.route("/ask_pdf", methods=["POST"])
def ai_ask_pdf():

    data = request.json
    question = data.get("question")

    if not question:
        return jsonify({"error": "Question is required"}), 400

    result = generate_answer(question)

    return jsonify({
        "question": question,
        "answer": result["answer"],
        "sources": result["sources"]
    })
