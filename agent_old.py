
import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from .env")

# Initialize Gemini
client = genai.Client(api_key=API_KEY)


class StudyMateAgent:

    def __init__(self):
        self.model = "gemini-3.1-flash-lite"

        self.system_prompt = """
        You are StudyMate AI, an intelligent student assistant.

        Your responsibilities:
        - Explain academic topics.
        - Provide English and Bangla explanations.
        - Generate MCQ quizzes.
        - Summarize study notes.
        - Help students prepare for exams.
        - Create study plans.

        Always be friendly, accurate and educational.
        """

    def ask(self, question: str) -> str:

        for attempt in range(3):

            try:
                response = client.models.generate_content(
                    model=self.model,
                    contents=[
                        self.system_prompt,
                        f"Student question: {question}"
                    ]
                )

                return response.text or "No response generated."

            except errors.ServerError:

                if attempt == 2:
                    return "Gemini server is busy. Try again later."

                wait_time = 2 ** (attempt + 1)

                print(
                    f"Server busy. Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)

            except errors.APIError as e:

                return f"Gemini API Error: {e}"

        return "Unable to generate response."


# Create agent instance
agent = StudyMateAgent()
