from argon2 import PasswordHasher, exceptions

class PasswordManager:
    ph = PasswordHasher()

    @classmethod
    def hash_password(cls, password: str) -> str:
        return cls.ph.hash(password)

    @classmethod
    def verify_password(cls, hash: str, password: str) -> bool:
        try:
            return cls.ph.verify(hash, password)
        except exceptions.VerifyMismatchError:
            return False
