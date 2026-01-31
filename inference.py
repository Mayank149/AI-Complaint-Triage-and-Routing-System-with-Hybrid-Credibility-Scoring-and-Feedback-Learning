import joblib
import os


#paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models")

DEPARTMENT_MODEL_PATH = os.path.join(MODEL_PATH, "department_model_v1.pkl")
URGENCY_MODEL_PATH = os.path.join(MODEL_PATH, "urgency_model_v1.pkl")

#loading the models using joblib
def load_model(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model file not found at {path}")
    with open(path, "rb") as f:
        return joblib.load(f)


department_pipeline = load_model(DEPARTMENT_MODEL_PATH)
urgency_pipeline = load_model(URGENCY_MODEL_PATH)

#function to predict the department and urgency

def predict_complaint(text):
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Invalid input. Please provide a non-empty string.")

    #department prediction
    dept_probs = department_pipeline.predict_proba([text])[0]
    dept_classes = department_pipeline.classes_

    dept_idx = dept_probs.argmax()
    predicted_department = dept_classes[dept_idx]
    department_confidence = dept_probs[dept_idx]

    #urgency prediction
    urg_probs = urgency_pipeline.predict_proba([text])[0]
    urg_classes = urgency_pipeline.classes_

    urg_idx = urg_probs.argmax()
    predicted_urgency = urg_classes[urg_idx]
    urgency_confidence = urg_probs[urg_idx]

    return {
        "department" : predicted_department,
        "department_confidence" : round(department_confidence, 3),
        "urgency" : predicted_urgency,
        "urgency_confidence" : round(urgency_confidence, 3)
    }

if __name__ == "__main__":
    print("Department model loaded:", type(department_pipeline))
    print("Urgency model loaded:", type(urgency_pipeline))

    sample_text = (
        "VPN keeps disconnecting during remote work. "
        "Happens every 20 minutes while on meetings."
    )

    result = predict_complaint(sample_text)
    print(result)