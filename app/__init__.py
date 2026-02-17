from flask import Flask
from app.rag.rag_service import RAGService
from app.services.static_service import get_static_files_paths
from .database import db
from .route import main


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chat.db"

    db.init_app(app)

    pdf_files_path = get_static_files_paths(app, "pdf")
    app.app_rag = RAGService(pdf_files_path)

    with app.app_context():
        db.create_all()

    app.register_blueprint(main)

    return app
