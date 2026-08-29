from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError


class Auth:
    _hasher = PasswordHasher()

    @staticmethod
    def hash_password(password: str) -> str:
        return Auth._hasher.hash(password)
