from fastapi import APIRouter, Depends
from app_back.db import get_db
from app_back.models import Meme
from app_back.schemas import MemeCreate, MemeUpdate

router = APIRouter()


@router.get("/memes", response_model=list[Meme])
async def get_memes(db: AsyncSession = Depends(get_db)):
    memes = await db.execute(select(Meme))
    return memes.scalars().all()


@router.get("/memes/{id}", response_model=Meme)
async def get_meme(id: int, db: AsyncSession = Depends(get_db)):
    meme = await db.get(Meme, id)
    if not meme:
        raise HTTPException(status_code=404, detail="Meme not found")
    return meme


@router.post("/memes", response_model=Meme)
async def create_meme(meme: MemeCreate, db: AsyncSession = Depends(get_db)):
    new_meme = Meme(**meme.dict())
    db.add(new_meme)
    await db.commit()
    await db.refresh(new_meme)
    return new_meme


@router.put("/memes/{id}", response_model=Meme)
async def update_meme(id: int, meme: MemeUpdate, db: AsyncSession = Depends(get_db)):
    meme_obj = await db.get(Meme, id)
    if not meme_obj:
        raise HTTPException(status_code=404, detail="Meme not found")
    for field, value in meme.dict().items():
        setattr(meme_obj, field, value)
    await db.commit()
    await db.refresh(meme_obj)
    return meme_obj


@router.delete("/memes/{id}")
async def delete_meme(id: int, db: AsyncSession = Depends(get_db)):
    meme = await db.get(Meme, id)
    if not meme:
        raise HTTPException(status_code=404, detail="Meme not found")
    await db.delete(meme)
    await db.commit()
    return {"message": "Meme deleted successfully"}
