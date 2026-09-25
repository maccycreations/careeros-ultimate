"""Authentication helpers for local-first login and user session state."""
from typing import Optional

from passlib.context import CryptContext
from sqlmodel import Session, select

from models import User, engine

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def create_user(email: str, name: str, password: str) -> User:
    email = email.strip().lower()
    with Session(engine) as session:
        existing = session.exec(select(User).where(User.email == email)).first()
        if existing:
            return existing
        user = User(email=email, name=name.strip() or email.split('@')[0], password_hash=hash_password(password))
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


def authenticate_user(email: str, password: str) -> Optional[User]:
    with Session(engine) as session:
        user = session.exec(select(User).where(User.email == email.strip().lower())).first()
        if user and verify_password(password, user.password_hash):
            return user
    return None


def get_or_create_demo_user() -> User:
    return create_user("demo@maccy.com", "Demo User", "careerx123")


def get_current_user():
    from nicegui import ui

    user_id = ui.storage.user.get("careerx_user_id")
    if not user_id:
        return None
    with Session(engine) as session:
        return session.get(User, int(user_id))


def set_current_user(user: User):
    from nicegui import ui

    ui.storage.user["careerx_user_id"] = user.id


def logout_user():
    from nicegui import ui

    ui.storage.user.clear()
