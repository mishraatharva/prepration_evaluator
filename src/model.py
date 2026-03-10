from pydantic import BaseModel
from typing import List

class AnswerRequest(BaseModel):
    session_id: str
    question_id: str
    answer: str


class QuestionResponse(BaseModel):
    question_id: str
    question: str
    options: List[str]