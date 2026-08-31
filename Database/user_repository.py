from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from Database.config_db import db
from models.schemas import User, UserOut
from models.enums import UserRole
from Database.db_schemas import UsersTable
from sqlalchemy.exc import IntegrityError

Session = sessionmaker(bind=db)


class UserRepository:
    @staticmethod
    def create_user(login: str, password_hash: str, role: UserRole) -> UserOut:
        # Takes an already-hashed password: the repository never sees plaintext.
        with Session() as session:
            new_user = UsersTable(
                role=role.value,
                login=login,
                password=password_hash,
                is_active=True,
            )
            session.add(new_user)
            try:
                # the UNIQUE constraint on login fires HERE, not on construction
                session.commit()
            except IntegrityError as e:
                session.rollback()
                raise ValueError(f"Login '{login}' already exists.") from e
            # built while the session is still open, so the row is not detached
            return UserOut.model_validate(new_user)

    @staticmethod
    def fetch_for_login_check(login: str) -> User | None:
        with Session() as session:
            stmt = session.scalar(
                select(UsersTable).where(UsersTable.login == login)
            )
            if stmt:
                return User(
                    id=stmt.id,
                    role=stmt.role,
                    login=stmt.login,
                    password=stmt.password,
                    is_active=stmt.is_active,
                )
            return None

    @staticmethod
    def update_role(user_login: str, new_role: str) -> bool:
        with Session() as session:
            stmt = session.scalar(
                select(UsersTable).where(UsersTable.login == user_login)
            )
            if not stmt:
                return False
            stmt.role = new_role
            session.commit()
            return True