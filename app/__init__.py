from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.secret_key = "uhhhhIllmakethissafelater" #os.getenv("SECRET_KEY", "uhhhhIllmakethissafelater")

    from .routes import main
    app.register_blueprint(main)
    return app
