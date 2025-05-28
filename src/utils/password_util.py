from passlib.context import CryptContext


password_context = CryptContext(
    schemes=['bcrypt']
)

def generate_password_hash(password:str)->str:
    return password_context.hash(password)

def verify_password(secret:str, hash_password:str):
    return password_context.verify(secret,hash_password)