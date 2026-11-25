
from agent import agent

print("================================")
print("       StudyMate AI Agent")
print("================================")

while True:

    question = input("\nYou: ")

    if question.lower() in ["exit", "quit"]:
        print("StudyMate AI: Goodbye!")
        break

    print("\nStudyMate AI is thinking...\n")

    answer = agent.ask(question)

    print("\nStudyMate AI:")
    print(answer)
