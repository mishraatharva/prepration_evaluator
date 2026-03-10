import os

# Mongo URI
MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb+srv://atharva007:atharva007@prepration-evaluator-cl.59zqj5t.mongodb.net/?appName=prepration-evaluator-clustor"
)

# Database
DB_NAME = "gre-question-bank"

# Collections
QUESTIONS_COLLECTION = "gre_questions"
SESSIONS_COLLECTION = "user_sessions"
ATTEMPTS_COLLECTION = "attempts"

# Adaptive Test
TOTAL_QUESTIONS = 5