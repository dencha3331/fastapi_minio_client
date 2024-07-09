from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ... import crud, schemas, dependencies


router = APIRouter()


@router.get("/memes", response_model=List[schemas.Meme])
def read_memes(skip: int = 0, limit: int = 10, db: Session = Depends(dependencies.get_db)):
    memes = crud.get_memes(db, skip=skip, limit=limit)
    return memes


@router.get("/memes/{meme_id}", response_model=schemas.Meme)
def read_meme(meme_id: int, db: Session = Depends(dependencies.get_db)):
    db_meme = crud.get_meme(db, meme_id=meme_id)
    if db_meme is None:
        raise HTTPException(status_code=404, detail="Meme not found")
    return db_meme


@router.post("/memes", response_model=schemas.Meme)
def create_meme(meme: schemas.MemeCreate, db: Session = Depends(dependencies.get_db)):
    image_url = "http://s3-service-url/" + "image_path"  # Здесь вы будете загружать изображение на S3 и получать URL
    return crud.create_meme(db=db, meme=meme, image_url=image_url)


@router.put("/memes/{meme_id}", response_model=schemas.Meme)
def update_meme(meme_id: int, meme: schemas.MemeUpdate, db: Session = Depends(dependencies.get_db)):
    db_meme = crud.update_meme(db, meme_id=meme_id, meme=meme)
    if db_meme is None:
        raise HTTPException(status_code=404, detail="Meme not found")
    return db_meme


@router.delete("/memes/{meme_id}", response_model=schemas.Meme)
def delete_meme(meme_id: int, db: Session = Depends(dependencies.get_db)):
    db_meme = crud.delete_meme(db, meme_id=meme_id)
    if db_meme is None:
        raise HTTPException(status_code=404, detail="Meme not found")
    return db_meme
