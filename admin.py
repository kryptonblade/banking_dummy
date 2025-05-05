from database import db
from auth import hash_password
import re

ADMIN_USER = 'admin'
ADMIN_PASS_HASH = hash_password('password123')


def authenticate_admin(username: str, password: str) -> bool:
    return username == ADMIN_USER and hash_password(password) == ADMIN_PASS_HASH


def list_users() -> list:
    return list(db.keys())


def get_user_details(email: str):
    return db.get(email)


def delete_user(email: str) -> bool:
    if email in db:
        del db[email]
        return True
    return False