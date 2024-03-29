from passlib.context import CryptContext, CryptPolicy

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password) :
    return pwd_context.hash(password)

def validate_password(password, hash_password) :
    return pwd_context.verify(password, hash_password)

