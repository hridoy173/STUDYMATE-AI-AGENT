from agent import agent

result = agent.generate_quiz(
    topic="Computer Networks",
    number_of_questions=5,
    difficulty="Easy",
    language="English"
)

if result["success"]:

    print("\nQuiz generated successfully!")
    print("Topic:", result["topic"])
    print("Total Questions:", result["total_questions"])

    for index, question in enumerate(result["questions"], start=1):

        print(f"\nQuestion {index}:")
        print(question["question"])

        for option_index, option in enumerate(
            question["options"],
            start=1
        ):
            print(f"{option_index}. {option}")

        print("Correct Answer:", question["correct_answer"])
        print("Explanation:", question["explanation"])

else:

    print("\nQuiz generation failed:")
    print(result["error"])



## old code for testing quiz_generator function in tools.py
# from tools import quiz_generator

# questions = [
#     {
#         "question": "What does CPU stand for?",
#         "options": [
#             "Central Processing Unit",
#             "Computer Personal Unit",
#             "Central Program Utility",
#             "Control Processing Unit"
#         ],
#         "correct_answer": "A",
#         "explanation": "CPU stands for Central Processing Unit."
#     },
#     {
#         "question": "Which layer handles routing in the OSI model?",
#         "options": [
#             "Physical Layer",
#             "Network Layer",
#             "Session Layer",
#             "Application Layer"
#         ],
#         "correct_answer": "Network Layer",
#         "explanation": "The Network Layer handles logical addressing and routing."
#     }
# ]

# result = quiz_generator("Computer Networks", questions)

# print(result)
