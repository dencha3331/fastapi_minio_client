from __future__ import annotations

from fastapi import APIRouter, UploadFile, File, Depends
from pydantic import ValidationError

from apis.media.minio_client import upload_to_minio
from apis.memes.memes_main import add_meme_to_db_and_storage, get_memes
from models.schemas.memes_schemas import MemeCreate

router = APIRouter()

# , response_model=List[schemas.Meme]
@router.get("/memes")
async def read_memes(skip: int = 0, limit: int = 10):
    # memes = crud.get_memes(db, skip=skip, limit=limit)
    try:
        await get_memes(skip, limit)
        return {
            "skip": skip,
            "limit": limit,
            # "meme": get_memes(skip, limit)
        }
    except Exception as e:
        return {"error": f"{e!r}"}


# @router.get("/")
# async def index() -> dict[str, str]:
#     headers = {
#         'Content-Disposition': 'attachment; filename="filename.xlsx"'
#     }
#     files = get_memes()
#     return {
#         "info": "This is the index page of fastapi-nano. "
#         "You probably want to go to 'http://<hostname:port>/docs'.",
#     }

#
# @router.get("/memes/{id}", tags=["api_a"])
# async def view_a(
#     num: int,
#     auth: Depends = Depends(get_current_user),
# ) -> dict[str, int]:
#     return main_func_a(num)


@router.post("/memes")
async def create_meme(data: MemeCreate = Depends()):
    # return {
    #     "length": data.image.size
    # }
    return await add_meme_to_db_and_storage(data)


# @router.post("/memes")
# async def create_meme(file: UploadFile):
    # try:
    #     print(file.filename.split(".")[-1], file.content_type, file.file.name)
    #     # await upload_to_minio(file)
    #     await add_meme_to_db_and_storage(file)
    #     return {"message": f"Meme created successfully {file.filename}"}
    # except ValidationError as e:
    #     return {"error": str(e)}
    # try:
    #     return await add_meme_to_db_and_storage(data)
    #     # if file:
    #     #     # Обработка данных изображения
    #     #     # ...
    #     #     image_data = await file.read()
    #     #     image_model = ImageModel(image_data=image_data)
    #     #     # Валидация данных изображения
    #     #     image_model.validate()
    #     #     # Загрузка изображения в хранилище
    #     #     # ...
    #     #     # Сохранение URL изображения в данных MemeCreate
    #     #     data.image_url = "http://s3-service-url/" + "image_path"
    #     # # Валидация данных MemeCreate
    #     # data.validate()
    #     # # Сохранение мема в базе данных
    #     # await add_meme_to_db_and_storage(data)
    #     # print(data.file.filename, data.description)
    #     # return {"message": "Мем создан успешно"}
    # except Exception as e:
    #     return {"error": str(e)}