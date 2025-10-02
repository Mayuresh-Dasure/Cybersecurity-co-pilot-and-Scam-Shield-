import re
import json

# --- Parse syslog lines ---
def parse_syslog_line(line: str) -> dict:
    pattern = r"(?P<timestamp>^\w+\s+\d+\s[\d:]+)\s(?P<host>\S+)\s(?P<service>\S+)\[(?P<pid>\d+)\]:\s(?P<message>.+)"
    match = re.match(pattern, line)
    if match:
        return match.groupdict()
    return {"raw": line.strip()}

# --- Detect scam message ---
def detect_scam_message(msg: str) -> dict:
    scam_keywords = ["lottery", "bank", "blocked", "click here", "verify"]
    is_scam = any(word.lower() in msg.lower() for word in scam_keywords)
    return {
        "text": msg.strip(),
        "scam": is_scam,
        "reason": "Suspicious keywords found" if is_scam else "No scam detected"
    }

# --- Save output as JSON ---
def save_json(data, path="outputs/output.jsonl"):
    with open(path, "a") as f:
        f.write(json.dumps(data) + "\n")
