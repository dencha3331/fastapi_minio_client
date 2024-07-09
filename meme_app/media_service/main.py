from fastapi import FastAPI, File, UploadFile
from .s3_client import upload_to_s3

app = FastAPI()


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_location = f"/tmp/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(file.file.read())

    file_url = upload_to_s3(file_location, "memes")
    if not file_url:
        return {"error": "Failed to upload file"}

    return {"url": file_url}
