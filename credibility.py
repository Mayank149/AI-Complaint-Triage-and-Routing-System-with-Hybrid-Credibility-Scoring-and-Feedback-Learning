import re

def has_time_reference(text):
    patterns = [
        r"\b\d{1,2}:\d{2}\b",
        r"\b(today|yesterday|tomorrow)\b",
        r"\b(morning|evening|night)\b",
        r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
        r"\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\b",
        r"\b(january|february|march|april|may|june|july|august|september|october|november|december)\b",
        r"\b\d{4}\b",
        r"\b\d{1,2}\s+(?:minutes?|hours?|days?|weeks?|months?|years?)\s+ago\b",
        r"\b\d{1,2}\s+(?:minutes?|hours?|days?|weeks?|months?|years?)\s+from\s+now\b"
    ]
    return any(re.search(p, text, re.IGNORECASE) for p in patterns)

def has_location_reference(text):
    keywords = [
        "room", "hostel", "block", "floor",
        "office", "lab", "library", "gate"
    ]
    return any(word in text.lower() for word in keywords)

def has_identifier(text):
    patterns = [
        r"\broll\s*no\b",
        r"\bid\b",
        r"\bticket\b",
        r"\btransaction\b",
        r"\bcomplaint\s*id\b"
    ]
    return any(re.search(p, text, re.IGNORECASE) for p in patterns)


def has_evidence(text):
    keywords = [
        "screenshot", "photo", "image",
        "attached", "attachment", "video"
    ]
    return any(word in text.lower() for word in keywords)


def compute_rule_credibility(text):
    score = 0
    text_lower = text.lower()

    #Checking length
    if len(text.strip()) >= 50:
        score += 20
    elif len(text.strip()) < 20:
        score -= 40
    
    #Positive Signals
    if has_time_reference(text):
        score += 20
    if has_location_reference(text):
        score += 20
    if has_identifier(text):
        score += 20
    if has_evidence(text):
        score += 20

    #Negative vague/emotional patterns
    vague_patterns = [
        "please help",
        "asap",
        "very bad",
        "not acceptable",
        "worst",
        "angry",
        "frustrated"
    ]

    if any(p in text_lower for p in vague_patterns):
        score -= 20
    
    #clamping score between 0 and 100
    return max(0, min(100, score))

def compute_hybrid_credibility(rule_score, department_confidence, urgency_confidence, rule_weight = 0.7, ml_weight = 0.3):
    ml_confidence = (department_confidence + urgency_confidence) / 2
    ml_score = ml_confidence * 100
    final_score = (rule_weight * rule_score) + (ml_weight * ml_score)

    final_score = max(0, min(100,round(final_score, 2)))
    return final_score


if __name__ == "__main__":
    sample = (
        "Internet issue in hostel room 204 yesterday evening. "
        "Screenshot attached."
    )
    print("Credibility score:", compute_rule_credibility(sample))
