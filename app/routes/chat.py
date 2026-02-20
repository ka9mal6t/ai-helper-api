from flask import Blueprint, Response, stream_with_context, request
from app.services.rag import generate_answer_stream
import ollama


chat = Blueprint("chat", __name__)


@chat.route("/chat", methods=["POST"])
def ai_chat():

    data = request.json
    question = data.get("question")

    return Response(
        stream_with_context(generate_answer_stream(question)),
        content_type="text/event-stream"
    )
