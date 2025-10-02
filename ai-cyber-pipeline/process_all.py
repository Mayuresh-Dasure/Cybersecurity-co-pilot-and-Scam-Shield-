import json
from pipeline import classify_threat, generate_summary_action
from utils import parse_syslog_line, save_json
import os

# --- Paths ---
log_file = "data/logs.txt"
message_file = "data/message.txt"
output_file = "outputs/combined_summary.json"

all_results = []

# --- Process Logs ---
if os.path.exists(log_file):
    with open(log_file, "r", encoding="utf-8") as f:
        logs = f.readlines()
else:
    logs = []

for line in logs:
    line = line.strip()
    if line:
        parsed = parse_syslog_line(line)
        classification = classify_threat(line, source="log")
        summary, action = generate_summary_action(line, classification)
        all_results.append({
            "type": "log",
            "raw": line,
            "parsed": parsed,
            "classification": classification,
            "summary": summary,
            "action": action
        })

# --- Process Messages ---
if os.path.exists(message_file):
    with open(message_file, "r", encoding="utf-8") as f:
        messages = f.readlines()
else:
    messages = []

for msg in messages:
    msg = msg.strip()
    if msg:
        classification = classify_threat(msg, source="message")
        summary, action = generate_summary_action(msg, classification)
        all_results.append({
            "type": "message",
            "text": msg,
            "classification": classification,
            "summary": summary,
            "action": action
        })

# --- Save combined results as human-readable JSON ---
os.makedirs(os.path.dirname(output_file), exist_ok=True)
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(all_results, f, ensure_ascii=False, indent=4)

print(f"✅ Combined summary saved to {output_file}")
