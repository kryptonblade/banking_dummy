import random, hashlib
from config import EMAIL_REGEX, PHONE_REGEX
from database import db, otp_store
from models import User


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def send_otp(email: str) -> None:
    otp = str(random.randint(100000, 999999))
    otp_store[email] = otp
    print(f"OTP sent to {email}: {otp}")


def verify_otp(email: str, input_otp: str) -> bool:
    return otp_store.get(email) == input_otp


def register_user(email: str, phone: str, password: str) -> str:
    if not EMAIL_REGEX.match(email):
        raise ValueError("Invalid email format.")
    if not PHONE_REGEX.match(phone):
        raise ValueError("Invalid phone number.")
    if email in db:
        raise ValueError("Email already registered.")
    # create initial user record without accounts
    pwd_hash = hash_password(password)
    db[email] = User(email=email, phone=phone, password_hash=pwd_hash)
    # initialize primary account
    db[email].accounts[phone] = 0.0
    send_otp(email)
    return "OTP sent successfully"


def confirm_registration(email: str, otp: str) -> str:
    if not verify_otp(email, otp):
        raise ValueError("Invalid OTP.")
    # registration complete
    return "Account created successfully"


def login(email: str, password: str) -> bool:
    user = db.get(email)
    if not user:
        return False
    return user.password_hash == hash_password(password)


def reset_password(email: str) -> str:
    if email not in db:
        raise ValueError("Email not found.")
    send_otp(email)
    return "Password reset OTP sent successfully"


def confirm_reset_password(email: str, otp: str, new_password: str) -> str:
    if not verify_otp(email, otp):
        raise ValueError("Invalid OTP.")
    db[email].password_hash = hash_password(new_password)
    return "Password reset successfully"