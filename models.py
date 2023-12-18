import sqlalchemy as sa
from sqladmin import ModelView
from sqlalchemy import ForeignKey

from sqlalchemy.orm import declared_attr, DeclarativeBase, mapped_column, Mapped, relationship

from datetime import datetime

from typing import Any


class BaseSQLAlchemyClass(DeclarativeBase):
    # Generate __tablename__ automatically
    id: Any
    __name__: str
    __abstract__ = True

    created_on = mapped_column(
        sa.DateTime(),
        default=datetime.now,
        nullable=True
    )
    updated_on = mapped_column(
        sa.DateTime(),
        default=datetime.now,
        onupdate=datetime.now,
        nullable=True
    )

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class UserModel(BaseSQLAlchemyClass):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        sa.Integer,
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[str] = mapped_column(
        sa.String(200),
    )
    email: Mapped[str] = mapped_column(
        sa.String(300),
        default=None,
        nullable=True,
    )
    posts_model = relationship('PostModel', back_populates='user')


class PostModel(BaseSQLAlchemyClass):
    __tablename__ = "users_posts"

    post_id: Mapped[int] = mapped_column(
        sa.Integer,
        primary_key=True,
        autoincrement=True,
    )
    content: Mapped[str] = mapped_column(
        sa.String(3000),
        default='something',
        nullable=False,
    )
    created_on = mapped_column(
        sa.DateTime(),
        default=datetime.now,
        nullable=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'),
    )
    title: Mapped[str] = mapped_column(
        sa.String(200),
    )
    user = relationship('UserModel', back_populates='posts_model')


class UserAdmin(ModelView, model=UserModel):
    pass
