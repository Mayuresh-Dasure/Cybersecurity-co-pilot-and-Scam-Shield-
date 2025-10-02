# backend/app.py (Final Clean Version for Day 3)
from flask import Flask, request, jsonify
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})


@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    data = request.get_json()
    input_text = data.get('text', '') if data else ''
    
    # Logic to decide severity based on keywords
    if "ssh login" in input_text.lower() or "failed" in input_text.lower():
        severity_level = "High"
        summary_text = "Detected multiple failed SSH login attempts from IP 203.0.113.25. This indicates a possible brute-force attack."
        action_text = "iptables -A INPUT -s 203.0.113.25 -j DROP\nservice ssh restart"
        confidence_score = "92%"
    elif "scam" in input_text.lower() or "prize" in input_text.lower() or "click here" in input_text.lower():
        severity_level = "Medium"
        summary_text = "Identified suspicious phrasing common in phishing or scam messages. Exercise caution."
        action_text = "Do not click any links or reply. Block the sender and report the message."
        confidence_score = "88%"
    else:
        severity_level = "Low"
        summary_text = "Analysis complete. No immediate threats detected in the provided text."
        action_text = "No specific action required. Continue monitoring."
        confidence_score = "70%"

    response = {
        "summary": summary_text,
        "recommended_action": action_text,
        "confidence": confidence_score,
        "severity": severity_level
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=5000)