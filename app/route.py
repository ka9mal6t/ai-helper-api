from flask import Blueprint, render_template
from app.routes.ask import ask
from app.routes.ask_pdf import ask_pdf
from app.routes.chat import chat
from app.routes.chat_pdf import chat_pdf


main = Blueprint("main", __name__, url_prefix="/ai")

@main.route("/")
def index():
    return render_template("chat.html")

main.register_blueprint(ask)
main.register_blueprint(ask_pdf)
main.register_blueprint(chat)
main.register_blueprint(chat_pdf)