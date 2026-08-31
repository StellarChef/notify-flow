from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError
from Database.user_repository import UserRepository
from models.schemas import UserCreate, UserOut
from models.enums import UserRole


class Auth:
    _hasher = PasswordHasher()
    _DUMMY_HASH = _hasher.hash("unused-placeholder")

    @staticmethod
    def hash_password(password: str) -> str:
        return Auth._hasher.hash(password)

    @staticmethod
    def register(data: UserCreate) -> UserOut:
        # Hashing belongs here, not in the router: the plaintext password never
        # travels past this call. Every new account starts with no permissions.
        return UserRepository.create_user(
            login=data.login,
            password_hash=Auth.hash_password(data.password),
            role=UserRole.PENDING,
        )

    @staticmethod
    def verify_user(password: str, login: str) -> bool:
        user = UserRepository.fetch_for_login_check(login)
        # No early return: a missing user still goes through Argon2.
        stored = user.password if user else Auth._DUMMY_HASH

        try:
            Auth._hasher.verify(stored, password)
        except (VerifyMismatchError, InvalidHashError):
            return False

        # verify() passed - but passing against the dummy proves nothing.
        return user is not None
