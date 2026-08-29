from sqlalchemy import select
from sqlalchemy.orm import selectinload, sessionmaker
from Database.config_db import db
from models.schemas import User
from Database.db_schemas import UsersTable
from sqlalchemy.exc import IntegrityError

Session = sessionmaker(bind=db)


class UserRepository:
    @staticmethod
    def create_user(user: User) -> dict:
        with Session() as session:
            try:
                new_user = UsersTable(
                    role=user.role.value,
                    login=user.login,
                    password=user.password,
                    is_active=user.is_active,
                )
            except IntegrityError as e:
                raise ValueError(f"Login '{user.login}' already exists.") from e
            session.add(new_user)
            session.commit()
            return {"login": new_user.login}

    @staticmethod
    def fetch_for_login_check(login: str) -> User | None:
        with Session() as session:
            stmt = session.scalar(
                select(UsersTable)
                .where(UsersTable.login == login)
                .options(selectinload(UsersTable))
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
