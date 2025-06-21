from flask import current_app
from pymongo import MongoClient

db = None

def init_db(app):
    global db
    client = MongoClient(app.config['MONGO_URI'])
    db = client['softskill']

def get_db():
    return db
