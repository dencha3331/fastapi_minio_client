from PIL import Image
from fastapi import FastAPI, UploadFile, Form, HTTPException, status
from pydantic import BaseModel, ValidationError, validator, field_validator
from io import BytesIO

app = FastAPI()


# class ImageModel(BaseModel):
#     image_data: bytes  # Should contain image data
#
#     class Config:
#         arbitrary_types_allowed = True
#
#     @field_validator('image_data')
#     def check_image_data(cls, value):
#         try:
#             Image.open(BytesIO(value))
#         except Exception:
#             raise ValidationError("Invalid image data")
#         return value


class MemeCreate(BaseModel):
    description: str = Form(...)
    image: UploadFile = Form(...)

    @field_validator('image')
    @classmethod
    def check_file(cls, value: UploadFile):
        # if not value.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        #     raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        #                         detail='Invalid file extension. It should be .png, .jpg or .jpeg')
        # return value
        try:
            Image.open(value.file)
            return value
        except Exception:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail='Invalid file extension. It should be .png, .jpg or .jpeg')

    # @classmethod
    # def check_values(cls, description, file):
    #     print(f"{description =}")
    #     return cls(file=file, description=description)


class GetMemes(BaseModel):
    skip: int
    limit: int


# class Meme(MemeBase):
#     id: int
#     image_url: str
#
#     class Config:
#         orm_mode = True