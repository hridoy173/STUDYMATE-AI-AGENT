
from tools import study_planner

result = study_planner(
    subject="Computer Networks",
    topics=[
        "OSI Model",
        "TCP/IP Model",
        "Data Link Layer",
        "Flow Control",
        "Error Detection",
        "Routing"
    ],
    days=3,
    hours_per_day=2
)

print("StudyMate AI - Study Planner")
print("=" * 35)

if result["success"]:

    print("Subject:", result["subject"])
    print("Total Days:", result["total_days"])

    for day in result["study_plan"]:

        print(f"\nDay {day['day']}")

        for task in day["tasks"]:
            print(
                f"- {task['topic']}: "
                f"{task['duration_hours']} hours"
            )

        print("Total Hours:", day["total_hours"])

else:
    print("Error:", result["error"])
