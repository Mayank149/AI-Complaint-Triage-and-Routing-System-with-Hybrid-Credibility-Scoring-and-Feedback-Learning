from credibility import (
    has_time_reference,
    has_location_reference,
    has_identifier
)
import random

LOCATION_QUESTIONS = [
    "Can you specify the exact location where this issue occurred?",
    "Where exactly did this problem take place?",
    "Please mention the location related to this issue.",
    "Could you tell us the specific place where this happened?"
]

TIME_QUESTIONS = [
    "When did this issue occur?",
    "Can you share the date or time of the incident?",
    "Approximately when did this problem start?",
    "Do you remember when this issue happened?"
]

ELABORATION_QUESTIONS = [
    "Could you please provide more details about the issue?",
    "Can you elaborate a bit more so we can understand the problem better?",
    "Please add more details to help us investigate this issue.",
    "It would help if you could explain the issue in more detail."
]

IDENTIFIER_QUESTIONS = [
    "Do you have any relevant ID, ticket number, or reference number?",
    "Please provide any associated ID or reference number if available.",
    "Is there a ticket number, roll number, or transaction ID related to this?",
    "Can you share any identifier that can help us track this issue?"
]

def generate_followup_questions(text, max_questions=3):
    questions = []

    if not has_location_reference(text):
        questions.append(random.choice(LOCATION_QUESTIONS))
    
    if not has_time_reference(text):
        questions.append(random.choice(TIME_QUESTIONS))
    
    if len(text.strip()) < 50:
        questions.append(random.choice(ELABORATION_QUESTIONS))
    
    if not has_identifier(text):
        questions.append(random.choice(IDENTIFIER_QUESTIONS))

    return questions[:max_questions]


if __name__ == "__main__":
    sample = "Internet issue in hostel room 204 yesterday evening. Connection drops every 20 minutes."
    print(generate_followup_questions(sample))
