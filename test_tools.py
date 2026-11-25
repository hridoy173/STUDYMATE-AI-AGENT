
from tools import calculator

print("StudyMate AI - Calculator Tool")

while True:

    expression = input("\nEnter calculation (or exit): ")

    if expression.lower() == "exit":
        break

    result = calculator(expression)

    if result["success"]:
        print("Result:", result["result"])
    else:
        print("Error:", result["error"])
