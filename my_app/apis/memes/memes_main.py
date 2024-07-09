from pathlib import Path
from mimetypes import guess_type, guess_extension, MimeTypes
from typing import Sequence

from fastapi import UploadFile
from pydantic import ValidationError
from starlette.responses import FileResponse, StreamingResponse
from urllib3 import BaseHTTPResponse

from apis.media import minio_client
from models.db import crud
from models.db.models import Meme
# from models.db import crud
from models.schemas.memes_schemas import MemeCreate


async def get_memes(skip: int = 0, limit: int = 10):
    # memes = await crud.get_memes(skip=skip, limit=limit)
    # image_files = ["path/to/image1.jpg", "path/to/image2.jpg"]
    # responses = [FileResponse(str(image_file), media_type="image/jpeg") for image_file in image_files]
    # image_files = [Path("path/to/image1.jpg"), Path("path/to/image2.png"), ...]
    image_object: Sequence[Meme] = await crud.get_memes(skip=skip, limit=limit)
    image_files: Sequence[BaseHTTPResponse] = await minio_client.get_memes(image_object)  # решить с асинхронностью
    print(1, image_files)
    responses = []

    # return StreamingResponse(output, headers=headers)
    for image_file in image_files:
        responses.append(StreamingResponse(image_file))

    return responses


async def add_meme_to_db_and_storage(meme: MemeCreate):
    """"""
    try:
        file_name: str = meme.image.filename
        description: str = meme.description
        meme_db: Meme = await crud.add_meme(meme)
        # await upload_to_minio(
        #     file=meme.image.file, bucket_name=meme_db.bucket_name, file_name=meme_db.file_name
        # )
        return {
            "message": "Meme created successfully",
            "meme_id": f"{meme_db.id}"
        }
    except Exception as e:
        return {"error": f"{e!r}"}


# def get_file_format(file_data: bytes) -> str:
#     mime_types = MimeTypes()
#     media_type = mime_types.readfp(file_data)
#     if media_type is None:
#         return "unknown"
#     else:
#         return media_type


# def get_file_format(mime_type: str) -> str:
#     extension = guess_extension(mime_type)
#     if extension is None:
#         return "unknown"
#     else:
#         return extension
