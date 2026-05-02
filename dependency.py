from database.database import sessionLocal
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("FERNET_KEY")
if key is None:
    raise ValueError("FERNET_KEY is missing in .env")
cipher_suite = Fernet(key.encode())

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

def encrypt_pwd(password: str):
    encrypted_password = cipher_suite.encrypt(password.encode())
    return encrypted_password

def decrypt_pwd(encrypted_password: str):
    decrypted_password = cipher_suite.decrypt(encrypted_password.encode()).decode()
    return decrypted_password