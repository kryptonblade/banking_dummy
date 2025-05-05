import re

# Validation regex
EMAIL_REGEX = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")
PHONE_REGEX = re.compile(r"^\d{10}$")
LARGE_TXN_OTP_THRESHOLD = 50000.0  # ₹50,000
MIN_SAVINGS_BALANCE = 0.0  # ₹500