from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app_back.db.session import get_db
from app_back.schemas import MemeCreate, MemeUpdate


async def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_meme(db: Session, meme_id: int) -> Meme:
    meme = db.query(Meme).get(meme_id)
    if not meme:
        raise HTTPException(status_code=404, detail="Meme not found")
    return meme


async def create_meme(meme: MemeCreate, db: Session = Depends(get_db)) -> Meme:
    new_meme = Meme(**meme.dict())
    db.add(new_meme)
    await db.commit()
    await db.refresh(new_meme)
    return new_meme


async def update_meme(meme_id: int, meme: MemeUpdate, db: Session = Depends(get_db)) -> Meme:
    meme_obj = await get_meme(db, meme_id)
    for field, value in meme.dict().items():
        setattr(meme_obj, field, value)
    await db.commit()
    await db.refresh(meme_obj)
    return meme_obj


async def delete_meme(meme_id: int, db: Session = Depends(get_db)) -> dict:
    meme = await get_meme(db, meme_id)
    db.delete(meme)
    await db.commit()
    return {"message": "Meme deleted successfully"}