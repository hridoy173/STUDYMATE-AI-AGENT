
from tools import quiz_generator

questions = [
    {
        "question": "What does CPU stand for?",
        "options": [
            "Central Processing Unit",
            "Computer Personal Unit",
            "Central Program Utility",
            "Control Processing Unit"
        ],
        "correct_answer": "A",
        "explanation": "CPU stands for Central Processing Unit."
    },
    {
        "question": "Which layer handles routing in the OSI model?",
        "options": [
            "Physical Layer",
            "Network Layer",
            "Session Layer",
            "Application Layer"
        ],
        "correct_answer": "Network Layer",
        "explanation": "The Network Layer handles logical addressing and routing."
    }
]

result = quiz_generator("Computer Networks", questions)

print(result)
