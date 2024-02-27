from fastapi import Depends, APIRouter
from typing import List

from sqlalchemy.orm import Session

from app.models.flower import FlowerRequest, FlowerResponse, PatchFlowerRequest
from app.db.repositories import FlowersRepository
from app.api.auth import oath2_scheme, get_db


router = APIRouter()
flowers_repository = FlowersRepository()


@router.get("/", response_model=List[FlowerResponse])
def get_flowers(token: str = Depends(oath2_scheme), db: Session = Depends(get_db)):
    flowers = flowers_repository.get_all(db)
    return flowers
    
    
@router.post("/")
def post_flowers(flower: FlowerRequest, token: str = Depends(oath2_scheme), db: Session = Depends(get_db)):
    flower_id = flowers_repository.add_flower(db, flower)
    return flower_id


@router.patch("/{flower_id}", response_model=FlowerResponse)
def patch_flower(flower_id: int, flower_data: PatchFlowerRequest, token: str = Depends(oath2_scheme), db: Session = Depends(get_db)):
    updated_flower = flowers_repository.update_flower(db, flower_id, flower_data)
    return updated_flower  
    
    
@router.delete("/{flower_id}")
def delete_flower(flower_id: int, token: str = Depends(oath2_scheme), db: Session = Depends(get_db)):
    return flowers_repository.delete_flower(db, flower_id)
