def classify_threat(log_text):
    """
    Simple rule-based threat classifier.
    Returns severity, confidence, and suggested action.
    """
    severity = "Low"
    confidence = 50
    action = "Monitor the system."

    log_lower = log_text.lower()

    # Basic rules
    if "failed ssh" in log_lower or "login failed" in log_lower:
        severity = "Medium"
        confidence = 75
        action = "Check login attempts, consider blocking IP."
    if "brute force" in log_lower or "unauthorized access" in log_lower:
        severity = "High"
        confidence = 90
        action = "Immediate investigation and block suspicious IPs."
    if "phishing" in log_lower or "scam" in log_lower:
        severity = "High"
        confidence = 95
        action = "Alert users and block sender."

    return severity, confidence, action