import re
from database import db
from config import LARGE_TXN_OTP_THRESHOLD, PHONE_REGEX
from models import Transaction


def _find_user_by_account(account_number: str):
    for user in db.values():
        if account_number in user.accounts:
            return user
    return None


def add_account_to_user(email: str, account_number: str, initial_deposit: float = 0.0) -> str:
    user = db.get(email)
    if not user:
        raise ValueError("User not found.")
    if not PHONE_REGEX.match(account_number):
        raise ValueError("Invalid account number format.")
    if account_number in user.accounts:
        raise ValueError("Account number already exists for user.")
    user.accounts[account_number] = initial_deposit
    if initial_deposit > 0:
        user.transactions.append(Transaction(
            txn_type='deposit', amount=initial_deposit,
            details={'account': account_number}
        ))
    return "Account added successfully"


def view_balance(account_number: str) -> float:
    user = _find_user_by_account(account_number)
    if not user:
        raise ValueError("Invalid account number.")
    return user.accounts[account_number]


def deposit(account_number: str, amount: float) -> str:
    if amount <= 0:
        raise ValueError("Invalid deposit amount.")
    user = _find_user_by_account(account_number)
    if not user:
        raise ValueError("Invalid account number.")
    user.accounts[account_number] += amount
    user.transactions.append(Transaction(
        txn_type='deposit', amount=amount,
        details={'account': account_number}
    ))
    return f"Deposited Rs.{amount} successfully"


def transfer_between_own_accounts(source_account_number: str, destination_account_number: str, amount: float) -> str:
    if amount <= 0:
        raise ValueError("Invalid transfer amount.")
    user = _find_user_by_account(source_account_number)
    if not user or destination_account_number not in user.accounts:
        raise ValueError("Invalid account number.")
    if not user.can_withdraw(source_account_number, amount):
        raise ValueError("Insufficient funds (minimum balance requirement).")
    user.accounts[source_account_number] -= amount
    user.accounts[destination_account_number] += amount
    user.transactions.append(Transaction(
        txn_type='internal_transfer', amount=amount,
        details={'from': source_account_number, 'to': destination_account_number}
    ))
    return "Funds transferred successfully"


def interbank_transfer(source_account_number: str, destination_bank_account: str, amount: float) -> str:
    if amount <= 0:
        raise ValueError("Invalid transfer amount.")
    user = _find_user_by_account(source_account_number)
    if not user:
        raise ValueError("Invalid source account number.")
    if not user.can_withdraw(source_account_number, amount):
        raise ValueError("Insufficient funds (minimum balance requirement).")
    user.accounts[source_account_number] -= amount
    user.transactions.append(Transaction(
        txn_type='interbank', amount=amount,
        details={'from': source_account_number, 'to': destination_bank_account}
    ))
    if amount > LARGE_TXN_OTP_THRESHOLD:
        return "Notification sent successfully"
    return "Inter-bank transfer initiated successfully"


def generate_pdf_statement(account_number: str) -> str:
    user = _find_user_by_account(account_number)
    if not user:
        raise ValueError("Invalid account number.")

    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Statement for {account_number}", ln=True)
    pdf.ln(5)

    # List only transactions involving this account
    for txn in user.transactions:
        involved = False
        if txn.type == 'deposit' and txn.details.get('account') == account_number:
            involved = True
            desc = f"Deposit of Rs.{txn.amount}"
        elif txn.type == 'internal_transfer':
            if txn.details.get('from') == account_number:
                involved = True
                desc = f"Transferred Rs.{txn.amount} to {txn.details['to']}"
            elif txn.details.get('to') == account_number:
                involved = True
                desc = f"Received Rs.{txn.amount} from {txn.details['from']}"
        elif txn.type == 'interbank' and txn.details.get('from') == account_number:
            involved = True
            desc = f"Interbank Rs.{txn.amount} to {txn.details['to']}"
        if involved:
            pdf.cell(0, 8, txt=desc, ln=True)

    filename = f"statement_{account_number}.pdf"
    pdf.output(filename)
    return "Account statement downloaded successfully"