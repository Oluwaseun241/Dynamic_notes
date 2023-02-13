from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash():
    def get_password_hash(password: str):
        return pwd_context.hash(password)

    def verify_password(password: str, hashed_password):
        return pwd_context.verify(password, hashed_password)