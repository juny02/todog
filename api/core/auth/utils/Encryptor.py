from passlib.context import CryptContext

class Encryptor:
    def __init__(self, context: CryptContext):
        self.context = context

    def hash(self, secret: str) -> str:
        return self.context.hash(secret)

    def verify(self, plain: str, hashed: str) -> bool:
        return self.context.verify(plain, hashed)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
encryptor = Encryptor(context=pwd_context)

def verify_password(plain_password, hashed_password):
    return encryptor.verify(plain_password, hashed_password)

def get_hashed_password(password):
    return encryptor.hash(password)