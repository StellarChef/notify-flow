from datetime import datetime, timedelta, timezone
from typing import Annotated
import jwt
from dotenv import load_dotenv
import os
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from Database.user_repository import UserRepository
from models.enums import UserRole
from models.schemas import Token, User, UserCreate, UserLogin, UserOut
from Services.auth_service import Auth

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

router = APIRouter(prefix="/auth", tags=["auth"])

# Reads "Authorization: Bearer <token>" off the request. In /docs this shows an
# Authorize box you paste a token into - which matches our JSON login endpoint.
bearer_scheme = HTTPBearer()


def create_access_token(user: User) -> str:
    payload = {
        "sub": user.login,
        "role": user.role.value,
        "type": "access",
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc)
        + timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(data: UserCreate):
    # Thin on purpose: HTTP in, HTTP out. Hashing and the default role are
    # decided in Auth.register, so this stays the only layer that knows codes.
    try:
        return Auth.register(data)
    except ValueError as e:
        # 409 - the request was well formed, it just clashes with existing state
        raise HTTPException(status.HTTP_409_CONFLICT, str(e)) from e


@router.post("/login", response_model=Token)
def login(data: UserLogin):
    user = Auth.verify_user(password=data.password, login=data.login)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")

    access_token = create_access_token(user)
    return Token(access_token=access_token, token_type="bearer")


async def get_current_user(
    creds: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
) -> User:
    # Either returns a valid user or stops the request - never None, so every
    # endpoint downstream can trust what it gets.
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # creds.credentials is the raw token - HTTPBearer strips "Bearer ".
        # decode() checks the signature AND exp; both failures land here.
        payload = jwt.decode(creds.credentials, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError as e:
        raise credentials_exception from e

    login = payload.get("sub")
    if login is None:
        raise credentials_exception

    # Read fresh: the token was issued up to 15 minutes ago and the account may
    # have been deleted or demoted since.
    user = UserRepository.fetch_for_login_check(login)
    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    # 403, not 401: we know who they are, they are simply not allowed in. A 401
    # would tell the client to log in again, which would not help here.
    if not current_user.is_active:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Account is disabled")

    # PENDING means "registered, waiting for an admin" - no access to anything.
    if current_user.role is UserRole.PENDING:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Account awaiting approval")

    return current_user
