import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model="openai/gpt-oss-120b"
)


template = """
You are an expert GRE tutor.

A student completed an adaptive GRE practice test.

Student performance:

Ability Score: {ability}

Incorrect Questions:
{incorrect_questions}

Generate a clear 3 step personalized study plan to improve the student.

Make it practical and focused on GRE preparation.
"""

prompt = PromptTemplate(
    input_variables=["ability", "incorrect_questions"],
    template=template
)


chain = prompt | llm


def generate_learning_plan(ability, incorrect_questions):

    text = "\n".join(incorrect_questions)

    result = chain.invoke({
    "ability": ability,
    "incorrect_questions": text
})

    return result.content