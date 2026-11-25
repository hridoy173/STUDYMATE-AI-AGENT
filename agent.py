
import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types, errors

from tools import calculator

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from .env")

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

        TOOL RULES:
        - If the user asks for mathematical calculations,
          you MUST use the calculator tool.
        - Never calculate mathematical results yourself
          when the calculator tool is available.
        - Explain the final result clearly.

        Always be friendly and educational.
        """

        # Declare calculator tool for Gemini
        self.tools = [
            types.Tool(
                function_declarations=[
                    types.FunctionDeclaration(
                        name="calculator",
                        description=(
                            "Calculate a mathematical expression "
                            "using Python."
                        ),
                        parameters=types.Schema(
                            type=types.Type.OBJECT,
                            properties={
                                "expression": types.Schema(
                                    type=types.Type.STRING,
                                    description=(
                                        "Mathematical expression. "
                                        "Example: 8500 * 25 / 100"
                                    )
                                )
                            },
                            required=["expression"]
                        )
                    )
                ]
            )
        ]

    def ask(self, question: str) -> str:

        for attempt in range(3):

            try:

                # Step 1: Send user question to Gemini
                response = client.models.generate_content(
                    model=self.model,
                    contents=question,
                    config=types.GenerateContentConfig(
                        system_instruction=self.system_prompt,
                        tools=self.tools
                    )
                )

                # Step 2: Check whether Gemini requested a tool
                function_calls = response.function_calls

                if not function_calls:
                    return response.text or "No response generated."

                # Step 3: Execute requested Python tools
                function_responses = []

                for function_call in function_calls:

                    if function_call.name == "calculator":

                        args = function_call.args or {}

                        print("\n[Agent] Calculator tool selected")

                        result = calculator(
                            args["expression"]
                        )

                        print("[Tool] Result:", result)

                        function_responses.append(
                            types.Part.from_function_response(
                                name=function_call.name,
                                response=result
                            )
                        )

                # Step 4: Send tool result back to Gemini
                final_response = client.models.generate_content(
                    model=self.model,
                    contents=[
                        types.Content(
                            role="user",
                            parts=[
                                types.Part(text=question)
                            ]
                        ),
                        response.candidates[0].content,
                        types.Content(
                            role="user",
                            parts=function_responses
                        )
                    ],
                    config=types.GenerateContentConfig(
                        system_instruction=self.system_prompt,
                        tools=self.tools
                    )
                )

                # Step 5: Return final AI answer
                return (
                    final_response.text
                    or "Unable to generate final response."
                )

            except errors.ServerError:

                if attempt == 2:
                    return "Gemini server is busy. Try again later."

                wait_time = 2 ** (attempt + 1)

                print(
                    f"Server busy. Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)

            except (errors.APIError, KeyError, ValueError) as e:

                return f"Agent Error: {e}"

        return "Unable to generate response."


agent = StudyMateAgent()
