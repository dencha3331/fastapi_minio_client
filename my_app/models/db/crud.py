import uuid

from minio import S3Error, error
from sqlalchemy.exc import NoResultFound, MultipleResultsFound, PendingRollbackError
from sqlalchemy import exc as exceptions
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import ScalarResult
from sqlalchemy import select, update, delete, Select, insert
from typing import Sequence, BinaryIO

from apis.media.minio_client import upload_to_minio
from models.db.models import Meme, engine
from environs import Env

from models.schemas.memes_schemas import MemeCreate

env: Env = Env()
env.read_env()

async_session = async_sessionmaker(engine, expire_on_commit=False)


async def add_objects(*args) -> None:
    async with async_session() as session:
        session.add_all(args)
        await session.commit()


async def get_memes(skip: int = 0, limit: int = 10) -> Sequence[Meme] | None:
    stmt = select(Meme).offset(skip).limit(limit).order_by('id')
    async with async_session() as session:
        result = await session.scalars(stmt)
        try:
            return result.all()
        except Exception as e:
            return


async def add_meme(meme: MemeCreate, bucket_name: str = 'memes') -> Meme | None:
    """"""
    file_name: str = meme.image.filename
    description: str = meme.description
    image_file: BinaryIO = meme.image.file
    async with async_session() as session:
        new_meme = Meme()
        new_meme.bucket_name = bucket_name
        new_meme.description = description
        # new_meme.source_file_name = file_name
        for i in range(10):
            try:
                if i > 0:
                    file_name = f'{file_name.split(".")[0]}-{uuid.uuid4()}.{file_name.split(".")[-1]}'
                    print(file_name)
                new_meme.file_name = file_name
                new_meme.file_url = f"{'localhost:9000'}/{bucket_name}/{file_name}"
                session.add(new_meme)
                await session.flush()
                await upload_to_minio(
                    file=image_file, bucket_name=bucket_name, file_name=file_name
                )
                await session.commit()
                return new_meme
            except exceptions.IntegrityError as e:
                await session.rollback()
                if i >= 9:
                    raise e
            except error.S3Error as e:
                await session.rollback()
                raise e


