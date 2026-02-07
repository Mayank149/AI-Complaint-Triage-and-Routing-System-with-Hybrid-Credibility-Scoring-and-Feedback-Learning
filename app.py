from flask import Flask, request, jsonify
from flask_cors import CORS

from inference import predict_complaint
from credibility import compute_rule_credibility, compute_hybrid_credibility
from questions import generate_followup_questions
from db import init_db, insert_complaint, insert_feedback

app = Flask(__name__)
CORS(app)

init_db()

CREDIBILITY_THRESHOLD = 60

@app.route("/analyze-complaint", methods=["POST"])
def analyze_complaint():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error" : "Missing complaint text"}), 400
    
    text = data["text"]

    try:
        inference_result = predict_complaint(text)
        rule_score = compute_rule_credibility(text)

        credibility_score = compute_hybrid_credibility(
            rule_score,
            inference_result["department_confidence"],
            inference_result["urgency_confidence"]
        )

        if credibility_score < CREDIBILITY_THRESHOLD:
            followup_questions = generate_followup_questions(text)
        else:
            followup_questions = []
        
        complaint_id = insert_complaint(
            text = text,
            predicted_department = inference_result["department"],
            department_confidence = inference_result["department_confidence"],
            predicted_urgency = inference_result["urgency"],
            urgency_confidence = inference_result["urgency_confidence"],
            credibility_score = credibility_score
        )

        response = {
            "department" : inference_result["department"],
            "department_confidence" : inference_result["department_confidence"],
            "urgency" : inference_result["urgency"],
            "urgency_confidence" : inference_result["urgency_confidence"],
            "credibility_score" : credibility_score,
            "followup_questions" : followup_questions,
            "complaint_id" : complaint_id
        }
        

        return jsonify(response)
    
    except Exception as e:
        return jsonify({"error" : str(e)}), 500

@app.route("/feedback", methods = ["POST"])
def submit_feedback():
    data = request.get_json()
    required_fields = ["complaint_id", "predicted_department", "correct_department", "predicted_urgency", "correct_urgency"]

    if not data or not all(field in data for field in required_fields):
        return jsonify({"error" : "Missing feedback fields"}), 400

    try:
        insert_feedback(
            complaint_id = data["complaint_id"],
            predicted_department = data["predicted_department"],
            correct_department = data["correct_department"],
            predicted_urgency = data["predicted_urgency"],
            correct_urgency = data["correct_urgency"]
        )

        return jsonify({"status" : "Feedback recorded successfully"})
    except Exception as e:
        return jsonify({"error" : str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)