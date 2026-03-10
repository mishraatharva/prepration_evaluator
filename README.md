# Adaptive GRE Test Platform

An AI-powered adaptive testing system that dynamically adjusts question difficulty based on a student's performance and generates a personalized learning plan using an LLM.

The system simulates the core concept used in standardized adaptive exams such as the GRE and GMAT, where the next question depends on the test taker's estimated ability.

---

## Features

- Adaptive question selection based on student ability
- Difficulty-adjusted GRE-style questions
- Real-time ability estimation
- MongoDB-based attempt tracking
- Personalized AI-generated study plan
- Full-stack implementation using FastAPI + JavaScript
- LLM integration using Groq + LangChain

---

## System Architecture

Frontend (HTML + JavaScript)

↓

FastAPI Backend

↓

Adaptive Engine

↓

MongoDB Question Bank

↓

Groq LLM (LangChain)

↓

Personalized Study Plan

---

## Adaptive Algorithm Logic

The adaptive engine maintains an **ability score between 0.1 and 1.0** representing the student's estimated proficiency.

Ability Update

If the answer is correct:

ability = ability + 0.1 * (1 - ability)

If the answer is incorrect:

ability = ability - 0.1 * ability

This gradually adjusts difficulty while keeping the ability score stable.

Question Selection

The next question is selected based on the student's estimated ability:

difficulty ∈ [ability - 0.1 , ability + 0.1]

If no question exists in this range, the system selects any unanswered question.

Already asked questions are excluded to avoid repetition.

---

## AI Personalized Learning Plan

After completing the test:

1. Incorrectly answered questions are identified.
2. The student's performance data is sent to a Groq LLM.
3. A 3-step personalized study plan is generated.

The prompt includes:

- Student ability score
- Incorrect questions
- Correct answers

The LLM returns targeted recommendations to improve weak areas.

---

## Tech Stack

Backend

- FastAPI
- Python
- MongoDB
- PyMongo

AI / LLM

- LangChain
- Groq API
- Prompt Engineering

Frontend

- HTML
- Vanilla JavaScript

---

## Installation & Setup

1. Clone the repository

git clone https://github.com/mishraatharva/prepration_evaluator.git
cd prepration_evaluator

2. Create virtual environment

python -m venv venv

3. Activate environment

Windows

venv\Scripts\activate

Mac / Linux

source venv/bin/activate

4. Install dependencies

pip install -r requirements.txt

5. Configure Environment Variables

Create `.env` file

GROQ_API_KEY=your_groq_api_key
UPDATE Mongo_db uri in sr.config

6. Run the application

uvicorn app:app --reload

Open in browser:

http://127.0.0.1:8000

---

## API Documentation

1. Start Test Session  
Endpoint: POST /start-session

Description:  
Creates a new adaptive test session and returns the first question.

Response Example:

{
  "session_id": "...",
  "question": "...",
  "options": [],
  "question_id": "..."
}

2. Submit Answer  
Endpoint: POST /submit-answer

Description:  
Submits the user's answer and returns the next adaptive question.

Request Example:

{
  "session_id": "...",
  "question_id": "...",
  "answer": "..."
}

Response:  
Returns the next question or test completion.

3. Generate AI Learning Plan  
Endpoint: GET /generate-report/{session_id}

Description:  
Generates a personalized study plan using an LLM based on the user's incorrect answers.

Response Example:

{
  "incorrect_questions": [...],
  "learning_plan": "3 step personalized study plan"
}

---

## MongoDB Data Storage

Each completed test attempt is stored with:

{
 "date": "2026-03-10",
 "session_id": "...",
 "ability": 0.63,
 "questions": [
   {
     "question": "...",
     "answer": "...",
     "correct_answer": "...",
     "correct": false
   }
 ],
 "created_at": "timestamp"
}

This enables:

- Progress tracking
- Performance analytics
- Adaptive learning history

---

## AI Development Log

AI-assisted tools were used during development to help with tasks such as prompt structuring, debugging framework integration issues, and refining the LLM pipeline.

While these tools accelerated parts of the implementation, several components required manual reasoning and debugging, especially around adaptive question selection logic, database queries, and LangChain integration with FastAPI.

This combination of AI assistance and iterative debugging helped ensure the system worked reliably end-to-end.

---

## Future Improvements

Potential enhancements include:

- Adding topic-level skill tracking
- Generating LLM explanations for incorrect answers
- Visualizing student progress analytics

---

## Author

Atharva Mishra

AI / Machine Learning Engineer  
Generative AI Developer