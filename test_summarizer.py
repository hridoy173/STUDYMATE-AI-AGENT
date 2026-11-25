
from tools import notes_summarizer

sample_notes = """
The OSI model stands for Open Systems Interconnection.
It is a conceptual framework used to understand network communication.
It contains seven layers: Physical, Data Link, Network,
Transport, Session, Presentation, and Application.
Each layer performs a specific function in data communication.
"""

result = notes_summarizer(sample_notes)

print("StudyMate AI - Notes Summarizer Tool")
print(result)
