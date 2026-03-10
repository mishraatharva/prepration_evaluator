from pymongo import MongoClient
from src.config import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)

db = client[DB_NAME]

questions_collection = db["gre_questions"]
attempts_collection = db["attempts"]