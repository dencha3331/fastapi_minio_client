from minio import Minio
from minio.error import S3Error

minio_client = Minio('minio:9000',
                     access_key='ROOTNAME',
                     secret_key='CHANGEME123',
                     secure=False)  # Установите secure=True, если используете HTTPS


def upload_to_minio(file_path, bucket_name, object_name=None):
    if object_name is None:
        object_name = file_path

    try:
        minio_client.fput_object(bucket_name, object_name, file_path)
        minio_client.put_object(bucket_name, object_name, file_path)
        return f"Uploaded {object_name} to {bucket_name} in Minio"
    except S3Error as err:
        return f"Minio upload error: {err}"
