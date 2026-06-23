import os

import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)


def test_gemini():
    return "Gemini Service Loaded"

def list_models():
    for model in genai.list_models():
        print(model.name)
        
def test_review():
    model = genai.GenerativeModel("gemini-2.5-flash")

    response = model.generate_content(
        "Review this code: print('hello world')"
    )

    return response.text

def review_pr(prompt):
    model = genai.GenerativeModel("gemini-2.5-flash")

    response = model.generate_content(prompt)

    return response.text