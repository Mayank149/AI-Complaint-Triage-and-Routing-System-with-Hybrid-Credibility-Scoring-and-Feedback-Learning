from flask import Flask, request, jsonify
from flask_cors import CORS

from inference import predict_complaint
from credibility import compute_rule_credibility
from questions import generate_followup_questions

app = Flask(__name__)
CORS(app)

CREDIBILITY_THRESHOLD = 60

@app.route("/analyze-complaint", methods=["POST"])
def analyze_complaint():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error" : "Missing complaint text"}), 400
    
    text = data["text"]

    try:
        inference_result = predict_complaint(text)
        credibility_score = compute_rule_credibility(text)

        if credibility_score < CREDIBILITY_THRESHOLD:
            followup_questions = generate_followup_questions(text)
        else:
            followup_questions = []
        
        response = {
            "department" : inference_result["department"],
            "department_confidence" : inference_result["department_confidence"],
            "urgency" : inference_result["urgency"],
            "urgency_confidence" : inference_result["urgency_confidence"],
            "credibility_score" : credibility_score,
            "followup_questions" : followup_questions
        }

        return jsonify(response)
    
    except Exception as e:
        return jsonify({"error" : str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)