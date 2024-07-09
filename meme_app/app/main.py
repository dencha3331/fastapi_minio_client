from fastapi import FastAPI
from .api.endpoints import memes

app = FastAPI()

app.include_router(memes.router, prefix="/apis/v1")