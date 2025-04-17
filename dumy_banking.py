# Project: Banking System Backend (Simplified Example)

# File: models.py
from dataclasses import dataclass, field
from typing import List

@dataclass
class User:
    email: str
    phone: str
    password: str
    balance: float = 0.0
    accounts: List[str] = field(default_factory=list)


# File: database.py
from typing import Dict
from models import User

db: Dict[str, User] = {}  # key: email, value: User object
otp_store: Dict[str, str] = {}  # key: email, value: otp


# File: auth.py
import random
from database import db, otp_store

def send_otp(email):
    otp = str(random.randint(100000, 999999))
    otp_store[email] = otp
    print(f"OTP sent to {email}: {otp}")  # Simulate sending

def verify_otp(email, input_otp):
    return otp_store.get(email) == input_otp

def register_user(email, phone, password):
    if email in db:
        raise ValueError("Email already registered.")
    send_otp(email)

def confirm_registration(email, phone, password, otp):
    if not verify_otp(email, otp):
        raise ValueError("Invalid OTP.")
    from models import User
    db[email] = User(email=email, phone=phone, password=password)
    return True

def login(email, password):
    user = db.get(email)
    return user and user.password == password

def reset_password(email):
    send_otp(email)

def confirm_reset_password(email, otp, new_password):
    if verify_otp(email, otp):
        db[email].password = new_password
        return True
    return False


# File: account.py
from database import db

def view_balance(email):
    return db[email].balance

def transfer_between_own_accounts(email, from_account, to_account, amount):
    # Mock behavior for internal transfer
    print(f"Transferred ₹{amount} from {from_account} to {to_account} for {email}")
    return True

def interbank_transfer(email, to_bank_account, amount):
    print(f"Interbank transfer of ₹{amount} initiated by {email} to {to_bank_account} (ETA: <24h)")
    if amount > 5000:
        notify_transaction(email, amount)
    return True

def notify_transaction(email, amount):
    print(f"Notification: ₹{amount} debited from your account. (Email/SMS sent to {email})")


# File: statements.py
from fpdf import FPDF

def generate_pdf_statement(email):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Account Statement for {email}", ln=True)
    pdf.cell(200, 10, txt="[Mock Transactions List]", ln=True)
    filename = f"statement_{email.replace('@', '_at_')}.pdf"
    pdf.output(filename)
    return filename


# File: admin.py
from database import db

def list_users():
    return list(db.keys())

def get_user_details(email):
    return db.get(email)

def delete_user(email):
    if email in db:
        del db[email]
        return True
    return False


# File: main.py
from auth import register_user, confirm_registration, login, reset_password, confirm_reset_password
from account import view_balance, transfer_between_own_accounts, interbank_transfer
from statements import generate_pdf_statement
from admin import list_users, get_user_details, delete_user

# Example Usage (Simulate interaction)
register_user("user@example.com", "9876543210", "pass123")
confirm_registration("user@example.com", "9876543210", "pass123", input("Enter OTP: "))
print("Login Success?", login("user@example.com", "pass123"))
print("Balance:", view_balance("user@example.com"))
transfer_between_own_accounts("user@example.com", "acc1", "acc2", 2000)
interbank_transfer("user@example.com", "ICICI1234", 6000)
print("PDF generated:", generate_pdf_statement("user@example.com"))
print("All users:", list_users())
