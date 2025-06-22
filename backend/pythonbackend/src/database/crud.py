from datetime import datetime, timezone, timedelta
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from src.database.models import User, UserAuth, MessageHistory
from src.schemas.message import MessageCreate
from src.schemas.user import UserContext, UserCreate, UserInDB


def get_user(db: Session, user_id: str):
    return db.query(User).filter(User.user_id == user_id).first()


def create_user(db: Session, user: UserCreate):
    db_user = User(user_id=user.user_id, design_id=user.design_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_design_id(db: Session, user: UserCreate):
    stmt = (
        update(User)
        .where(User.user_id == user.user_id)
        .values(design_id=user.design_id)
    )
    db.execute(stmt)
    db.commit()
    db_user = get_user(db, user.user_id)

    return db_user


def set_auth_token(
    db: Session,
    user_id,
    access_token,
    refresh_token,
    expires_in=None,
    scopes=None,
    updated_at=None,
    jsonfile=None,
):
    current_auth = db.query(UserAuth).filter(UserAuth.user_id == user_id).first()

    if current_auth:
        current_auth.access_token = access_token
        current_auth.full_token = jsonfile
        current_auth.expires_in = datetime.now(timezone.utc) + timedelta(seconds=14400)
        db.commit()
        db.refresh(current_auth)
        return current_auth

    auth = UserAuth(
        user_id=user_id,
        full_token=jsonfile,
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=expires_in,
        scope=scopes,
    )
    db.add(auth)
    db.commit()
    db.refresh(auth)
    return auth


def get_auth_token(db: Session, user_id):
    return db.query(UserAuth).filter(UserAuth.user_id == user_id).first()


def get_user_context(db: Session, user_id):
    stmt = (
        select(User, UserAuth)
        .join(User.auth)
        .filter(User.user_id == user_id)
        .order_by(UserAuth.expires_in)
    )
    user = db.execute(stmt).first()

    if not user:
        raise Exception()

    user_context = UserContext(
        user_id=user.User.user_id,
        design_id=user.User.design_id,
        access_token=user.UserAuth.access_token,
    )
    return user_context


def create_message(db: Session, message: MessageCreate):
    db_message = MessageHistory(
        user_id=message.user_id,
        session_id=message.session_id,
        role=message.role,
        content=message.content,
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def get_messages(db: Session, user_id, session_id):
    stmt = (
        select(MessageHistory)
        .where(
            MessageHistory.session_id == session_id
            and MessageHistory.user_id == user_id
        )
        .order_by(MessageHistory.timestamp)
    )
    messages = db.scalars(stmt).all()
    print(messages)
    return messages
