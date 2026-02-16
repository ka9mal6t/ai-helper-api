from flask import Flask
from .database import db
from .routes import main

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chat.db"

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(main)

    return app
