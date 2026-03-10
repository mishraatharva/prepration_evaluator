from fastapi import APIRouter, Request, FastAPI
from bson import ObjectId
from src.database import questions_collection, attempts_collection
from src.adaptive_engine import update_ability, get_next_question
from src.model import AnswerRequest
from src.config import TOTAL_QUESTIONS
from fastapi.templating import Jinja2Templates
from pathlib import Path
from datetime import datetime
from src.llm_service.llm_service import generate_learning_plan
import uuid
import os

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent
templates_dir = BASE_DIR / "templates"

app = FastAPI(title="Adaptive GRE Test", version="1.0")

templates = Jinja2Templates(directory=str(templates_dir))

session = {}


@app.get("/")
def load_ui(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/start-session")
def start_session():

    ability = 0.5
    question = get_next_question(ability, [])

    session_id = str(uuid.uuid4())

    session[session_id] = {
        "ability": ability,
        "questions_answered": [],
        "asked_questions": [str(question["_id"])],
        "completed": False
    }

    return {
        "session_id": session_id,
        "question": question["question"],
        "options": question["options"],
        "question_id": str(question["_id"])
    }


@app.post("/submit-answer")
def submit_answer(data: AnswerRequest):

    user_session = session[data.session_id]

    question = questions_collection.find_one(
        {"_id": ObjectId(data.question_id)}
    )

    correct = question["correct_answer"] == data.answer

    new_ability = update_ability(user_session["ability"], correct)

    user_session["ability"] = new_ability

    user_session["questions_answered"].append({
        "question_id": data.question_id,
        "question": question["question"],
        "answer": data.answer,
        "correct_answer": question["correct_answer"],
        "correct": correct
    })

    if len(user_session["questions_answered"]) >= TOTAL_QUESTIONS:

        user_session["completed"] = True

        today = datetime.utcnow().strftime("%Y-%m-%d")

        attempt_doc = {
            "date": today,
            "session_id": data.session_id,
            "ability": new_ability,
            "questions": user_session["questions_answered"],
            "created_at": datetime.utcnow()
        }

        attempts_collection.insert_one(attempt_doc)

        return {
            "test_completed": True,
            "final_ability": new_ability
        }

    next_question = get_next_question(
        new_ability,
        user_session["asked_questions"]
    )

    user_session["asked_questions"].append(str(next_question["_id"]))

    return {
        "session_id": data.session_id,
        "question": next_question["question"],
        "options": next_question["options"],
        "question_id": str(next_question["_id"])
    }


@app.get("/generate-report/{session_id}")
def generate_report(session_id: str):

    user_session = session[session_id]

    incorrect = [
        q for q in user_session["questions_answered"]
        if not q["correct"]
    ]

    incorrect_questions = [
        f"{q['question']} (Correct: {q['correct_answer']})"
        for q in incorrect
    ]

    plan = generate_learning_plan(
        user_session["ability"],
        incorrect_questions
    )

    return {
        "incorrect_questions": incorrect,
        "learning_plan": plan
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        reload=True
    )