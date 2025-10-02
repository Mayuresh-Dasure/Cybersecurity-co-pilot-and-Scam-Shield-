from flask import Flask, request, jsonify
from utils import parse_syslog_line, detect_scam_message, save_json

app = Flask(__name__)

# ------------------------------
# Threat Classification Function
# ------------------------------
def classify_threat(text, source="log"):
    result = {
        "source": source,
        "text": text,
        "threat": None,
        "severity": "Low"
    }

    if source == "log":
        if "Failed password" in text:
            result["threat"] = "Failed SSH login"
            result["severity"] = "Medium"
        elif "Accepted password" in text:
            result["threat"] = "Successful login"
            result["severity"] = "Low"
    elif source == "message":
        phishing_keywords = ["lottery", "prize", "claim", "free gift", "congratulations", "click here"]
        if any(word.lower() in text.lower() for word in phishing_keywords):
            result["threat"] = "Possible Phishing"
            result["severity"] = "High"
        else:
            result["threat"] = "Normal message"
            result["severity"] = "Low"
    
    return result

# ------------------------------
# Generate summary & action
# ------------------------------
def generate_summary_action(text, classification):
    summary = ""
    action = ""

    if classification["source"] == "log":
        if classification["threat"] == "Failed SSH login":
            summary = "Multiple failed SSH login attempts detected."
            action = f"Monitor IP and consider blocking: {text.split()[-4]}"  # crude IP extraction
        elif classification["threat"] == "Successful login":
            summary = "Successful login detected."
            action = "No immediate action required."
        else:
            summary = "Log entry normal."
            action = "No action required."
    else:  # message
        if classification["threat"] == "Possible Phishing":
            summary = "Potential phishing message detected."
            action = "Warn user and block sender if possible."
        else:
            summary = "Message appears safe."
            action = "No action required."
    
    return summary, action

# ------------------------------
# API Endpoints
# ------------------------------
@app.route("/ingest_log", methods=["POST"])
def ingest_log():
    data = request.json
    log_line = data.get("log", "")
    if not log_line:
        return jsonify({"error": "No log provided"}), 400
    parsed = parse_syslog_line(log_line)
    save_json(parsed, "outputs/logs.jsonl")
    return jsonify(parsed)

@app.route("/ingest_message", methods=["POST"])
def ingest_message():
    data = request.json
    message = str(data.get("message", ""))  # Force string
    if not message:
        return jsonify({"error": "No message provided"}), 400
    result = detect_scam_message(message)
    save_json(result, "outputs/messages.jsonl")
    return jsonify(result)

@app.route("/analyze", methods=["POST"])
def analyze_text():
    data = request.json
    text = str(data.get("text", ""))
    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Step 1: Rule-based classification
    if "password" in text or "login" in text:
        classification = classify_threat(text, source="log")
    else:
        classification = classify_threat(text, source="message")

    # Step 2: Generate summary + recommended action
    summary, action = generate_summary_action(text, classification)

    # Prepare response
    response = {
        "raw_text": text,
        "classification": classification,
        "ai_summary": summary,
        "recommended_action": action
    }

    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
