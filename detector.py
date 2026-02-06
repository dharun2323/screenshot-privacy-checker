import re

def detect_sensitive(text):
    text = text.lower()
    found = []

    # Aadhaar
    if ("aadhaar" in text or "aadhar" in text) and re.search(r"\b\d{4}\s?\d{4}\s?\d{4}\b", text):
        found.append("Aadhaar Number")

    # PAN Card (ABCDE1234F)
    if re.search(r"\b[a-z]{5}[0-9]{4}[a-z]\b", text):
        found.append("PAN Card Number")

    # OTP
    if "otp" in text and re.search(r"\b\d{4,6}\b", text):
        found.append("OTP")

    # Email
    if re.search(r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}", text):
        found.append("Email ID")

    # Bank Account (STRICT)
    if "bank" in text and re.search(r"\b\d{9,18}\b", text):
        found.append("Bank Account Number")

    return found
