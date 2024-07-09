from io import BytesIO
from typing import BinaryIO, Sequence

from fastapi import UploadFile
from minio import Minio
from minio.error import S3Error
from minio.helpers import ObjectWriteResult
from urllib3 import BaseHTTPResponse

from models.db.models import Meme

minio_client = Minio('localhost:9000',
                     access_key='ROOTNAME',
                     secret_key='CHANGEME123',
                     secure=False
                     )  # Установите secure=True, если используете HTTPS


async def upload_to_minio(file: BinaryIO, bucket_name: str, file_name: str) -> ObjectWriteResult:
    """"""
    bucket: bool = minio_client.bucket_exists(bucket_name)
    if not bucket:
        minio_client.make_bucket(bucket_name=bucket_name)
    object_write_result: ObjectWriteResult = minio_client.put_object(
        bucket_name=bucket_name, object_name=file_name, data=file, length=-1, part_size=10 * 1024 * 1024,
    )
    print(object_write_result.location)
    print(f"Uploaded {file_name} to {bucket_name} in Minio")
    return object_write_result


async def get_memes(meme_objects: Sequence[Meme]) -> Sequence[BaseHTTPResponse]:
    result = []
    print(meme_objects)
    for meme in meme_objects:
        obj: BaseHTTPResponse = minio_client.get_object(bucket_name=meme.bucket_name, object_name=meme.file_name)
        print(minio_client.get_presigned_url("GET",
                                             "memes",
                                             "first_bg.jpg",
                                             ))
        result.append(obj)
        a = obj
    return result
    #     [
    #     minio_client.get_object(bucket_name=meme.bucket_name, object_name=meme.file_name)
    #     for meme in meme_objects
    # ]

    # minio_client.get_object()

    # object_name = file.filename
    # file.name
    # try:
    #     # minio_client.fput_object(bucket_name, object_name, file_path)
    #     # bucket = minio_client.get_bucket_tags(bucket_name=bucket_name)
    #     bucket = minio_client.bucket_exists(bucket_name)
    #     if not bucket:
    #         minio_client.make_bucket(bucket_name=bucket_name)
    #     minio_client.put_object(
    #         bucket_name=bucket_name, object_name=file_name, data=file, length=file.tell()
    #     )
    #     print(f"Uploaded {file_name} to {bucket_name} in Minio")
    #     return f"Uploaded {file_name} to {bucket_name} in Minio"
    # except S3Error as err:
    #     print(f"Minio upload error: {err}")
    #     return f"Minio upload error: {err}"
