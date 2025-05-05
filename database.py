from typing import Dict
from models import User

db: Dict[str, User] = {}
otp_store: Dict[str, str] = {}