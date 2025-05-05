from dataclasses import dataclass, field
from typing import List,Dict
from config import MIN_SAVINGS_BALANCE


class Transaction:
    def __init__(self, txn_type: str, amount: float, details: Dict[str, str]):
        self.type = txn_type
        self.amount = amount
        self.details = details

class User:
    def __init__(self, email: str, phone: str, password_hash: str):
        self.email = email
        self.phone = phone
        self.password_hash = password_hash
        # Map each account_number to its balance
        self.accounts: Dict[str, float] = {}
        self.transactions: List[Transaction] = []

    def can_withdraw(self, account_number: str, amount: float) -> bool:
        balance = self.accounts.get(account_number, 0.0)
        return (balance - amount) >= MIN_SAVINGS_BALANCE