from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    JSON,
    Boolean,
)
from sqlalchemy.orm import Relationship, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, unique=True)
    design_id = Column(String, index=True, unique=True)
    is_active = Column(Boolean, default=True)

    messages = relationship("MessageHistory", back_populates="user")
    auth = Relationship("UserAuth", back_populates="user", uselist=False)


class UserAuth(Base):
    __tablename__ = "auth"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    full_token = Column(JSON, nullable=True)
    access_token = Column(String, nullable=False)
    refresh_token = Column(String, nullable=True)
    expires_in = Column(DateTime, nullable=True)
    scope = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    user = Relationship("User", back_populates="auth")


class MessageHistory(Base):
    __tablename__ = "message_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    session_id = Column(
        String, index=True, nullable=False
    )  # To group messages within a conversation
    role = Column(String, nullable=False)  # "user" or "agent"
    content = Column(JSON, nullable=False)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))

    user = relationship("User", back_populates="messages")
