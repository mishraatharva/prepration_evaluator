import random
from bson import ObjectId
from src.database import questions_collection
import random


def update_ability(current_ability, correct):

    if correct:
        current_ability = current_ability + 0.1 * (1 - current_ability)
    else:
        current_ability = current_ability - 0.1 * current_ability

    return max(0.1, min(1.0, current_ability))


def get_next_question(ability, asked_questions):

    asked_object_ids = [ObjectId(q) for q in asked_questions]

    query = {
        "_id": {"$nin": asked_object_ids},
        "difficulty": {
            "$gte": ability - 0.1,
            "$lte": ability + 0.1
        }
    }

    questions = list(questions_collection.find(query))

    # fallback if no difficulty match
    if not questions:
        questions = list(
            questions_collection.find({
                "_id": {"$nin": asked_object_ids}
            })
        )

    if not questions:
        return None

    return random.choice(questions)