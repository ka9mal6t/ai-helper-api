from flask import Blueprint
from app.routes.ask import ask
from app.routes.ask_pdf import ask_pdf
from app.routes.chat import chat


main = Blueprint("main", __name__, url_prefix="/ai")

main.register_blueprint(ask)
main.register_blueprint(ask_pdf)
main.register_blueprint(chat)