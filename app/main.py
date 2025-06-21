from flask import Flask
from flask_cors import CORS
from app.routes.course import course_bp
from app.utils.db import init_db
from dotenv import load_dotenv
from app.config import Config
import os

def create_app():
    # Load biến môi trường từ file .env
    load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))



    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    init_db(app)
    app.register_blueprint(course_bp, url_prefix='/api/courses')

    return app
