import asyncio
import datetime
from typing import List, Optional
from sqlalchemy import ForeignKey, BigInteger, String
from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from environs import Env

env: Env = Env()
env.read_env()
engine = create_async_engine(f"{env('DB')}+{env('DB_DIALECT')}:///{env('DB_PATH') if env else ''}")


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Meme(Base):
    __tablename__ = "memes_paths"
    # __tablename__ = "memes"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    file_name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column(nullable=True)
    bucket_name: Mapped[str]
    file_url: Mapped[str] = mapped_column(unique=True)
    # source_file_name: Mapped[str]

    def __str__(self):
        return self.file_name


# class SessionPyro(Base):
#     __tablename__ = "sessions"
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     session_name: Mapped[str] = mapped_column(unique=True)
#     phone: Mapped[str | None] = mapped_column(unique=True)
#     count_add_users_call: Mapped[int] = mapped_column(default=0)
#     time_a_hundred_call_add_users: Mapped[datetime.datetime] = mapped_column(
#         default=datetime.datetime.now()
#     )
#     busy: Mapped[bool] = mapped_column(default=False)
#     group_cont: Mapped[int] = mapped_column(default=0)
#     first_start: Mapped[datetime.datetime] = mapped_column(
#             default=datetime.datetime.now()
#         )
#     schedule_clear: Mapped[bool] = mapped_column(default=False)
#     flood: Mapped[bool] = mapped_column(default=False)
#     flood_time: Mapped[Optional[int]]
#     last_call_time: Mapped[Optional[datetime.datetime]] = mapped_column(
#         onupdate=datetime.datetime.now()
#     )
#     groups: Mapped[List['Groups'] | None] = relationship(
#         back_populates="session",
#         # cascade="all, delete-orphan"
#
#     )
#
#
# class Groups(Base):
#     __tablename__ = "groups"
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     tg_name: Mapped[str]
#     tg_id: Mapped[Optional[int]] = mapped_column(BigInteger(), unique=True)
#     task_num: Mapped[int] = mapped_column(BigInteger(), unique=True)
#     task_id: Mapped[int] = mapped_column(BigInteger(), unique=True)
#     group_url: Mapped[Optional[str]]
#     count_users: Mapped[int] = mapped_column(default=0)
#     creator_name: Mapped[str]
#     finished_create: Mapped[bool] = mapped_column(default=False)
#     create_date: Mapped[datetime.datetime] = mapped_column(
#         default=datetime.datetime.now()
#     )
#     session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"))
#     session: Mapped['SessionPyro'] = relationship(back_populates="groups")
#
#
# class SentMessages(Base):
#     __tablename__ = "sent_messages"
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     user_id: Mapped[Optional[int]] = mapped_column(BigInteger())
#     message_id: Mapped[Optional[int]] = mapped_column(BigInteger())
#     chat_id: Mapped[Optional[int]] = mapped_column(BigInteger())
#     user_name: Mapped[str] = mapped_column()
#     session_name: Mapped[str]
#     group_id: Mapped[int] = mapped_column(BigInteger())


async def create_table():
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


asyncio.run(create_table())
