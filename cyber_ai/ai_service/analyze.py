from flask import Flask, request, jsonify
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import json
from rules import classify_threat

app = Flask(__name__)

# -----------------------------
# Load Flan-T5 model once
# -----------------------------
model_name = "google/flan-t5-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# -----------------------------

def summarize_log(log_text):
    prompt = (
        "You are a cybersecurity expert.\n"
        "Summarize the following log in 1-2 sentences:\n"
        f"{log_text}"
    )
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        **inputs, 
        max_new_tokens=100, 
        num_beams=5, 
        early_stopping=True
    )
    summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return summary

# -----------------------------
# Helper function: Rule-based classification


# -----------------------------
# Flask API
# -----------------------------
@app.route("/analyze", methods=["POST"])
def analyze():
    """
    Expected JSON input:
    {
        "logs": ["log line 1", "log line 2", ...]
    }
    """
    data = request.get_json()
    logs = data.get("logs", [])
    results = []

    for log in logs:
        summary = summarize_log(log)
        severity, confidence, action = classify_threat(log)

        results.append({
            "log": log,
            "summary": summary,
            "severity": severity,
            "confidence": confidence,
            "action": action
        })

    # Save results to summaries.json
    with open("summaries.json", "w") as f:
        json.dump(results, f, indent=4)

    return jsonify(results)

# -----------------------------
# Run Flask app
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
