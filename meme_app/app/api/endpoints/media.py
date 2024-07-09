from fastapi import APIRouter, File, UploadFile
from typing import List

router = APIRouter()

@router.post("/upload/")
async def upload_files(files: List[UploadFile] = File(...)):
    return {"filenames": [file.filename for file in files]}