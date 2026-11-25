
import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types, errors

from tools import calculator, quiz_generator , notes_summarizer

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
        - If the user requests an MCQ quiz, use the quiz_generator tool.
        - Generate exactly the number of questions requested.
        - Each question must have exactly four options.
        - Include the correct answer and a short explanation.
        - Never invent quiz results after tool validation fails.
        - Summarize long study notes into concise summaries.
        - Identify important concepts and key points.
        - Explain difficult terms in simple English and Bangla.
        - When users request note summarization, use the notes_summarizer tool.

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
                    ),


                    types.FunctionDeclaration(
                        name="notes_summarizer",
                        description=(
                            "Prepare and validate student notes for summarization. "
                            "Use this tool when the user asks to summarize notes."
                        ),
                        parameters=types.Schema(
                            type=types.Type.OBJECT,
                            properties={
                                "text": types.Schema(
                                    type=types.Type.STRING,
                                    description="The complete study notes provided by the user."
                                )
                            },
                            required=["text"]
                        )
                    ),
                    
                    types.FunctionDeclaration(
                        name="quiz_generator",
                        description=(
                            "Validate and structure MCQ questions for a student quiz. "
                            "Use this tool when the user requests a quiz."
                        ),
                        parameters=types.Schema(
                            type=types.Type.OBJECT,
                            properties={
                                "topic": types.Schema(
                                    type=types.Type.STRING,
                                    description="The academic topic of the quiz."
                                ),
                                "questions": types.Schema(
                                    type=types.Type.ARRAY,
                                    items=types.Schema(
                                        type=types.Type.OBJECT,
                                        properties={
                                            "question": types.Schema(
                                                type=types.Type.STRING
                                            ),
                                            "options": types.Schema(
                                                type=types.Type.ARRAY,
                                                items=types.Schema(
                                                    type=types.Type.STRING
                                                )
                                            ),
                                            "correct_answer": types.Schema(
                                                type=types.Type.STRING
                                            ),
                                            "explanation": types.Schema(
                                                type=types.Type.STRING
                                            )
                                        },
                                        required=[
                                            "question",
                                            "options",
                                            "correct_answer",
                                            "explanation"
                                        ]
                                    )
                                )
                            },
                            required=["topic", "questions"]
                        )
                    )
                ]
            ),

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

                # for function_call in function_calls:

                #     if function_call.name == "calculator":

                #         args = function_call.args or {}

                #         print("\n[Agent] Calculator tool selected")

                #         result = calculator(
                #             args["expression"]
                #         )

                #         print("[Tool] Result:", result)

                #         function_responses.append(
                #             types.Part.from_function_response(
                #                 name=function_call.name,
                #                 response=result
                #             )
                #         )

                for function_call in function_calls:
                    args = function_call.args or {}

                    if function_call.name == "calculator":
                        print("\n[Agent] Calculator tool selected")
                        result = calculator(args["expression"])

                    elif function_call.name == "quiz_generator":
                        print("\n[Agent] Quiz Generator tool selected")
                        result = quiz_generator(
                            args["topic"],
                            args["questions"]
                        )

                    elif function_call.name == "notes_summarizer":
                        args = function_call.args or {}

                        print("\n[Agent] Notes Summarizer tool selected")

                        result = notes_summarizer(args["text"])

                    else:
                        continue

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
