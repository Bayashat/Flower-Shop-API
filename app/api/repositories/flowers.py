from typing import List
from fastapi import HTTPException

from sqlite3 import IntegrityError
from sqlalchemy.orm import Session

from app.api.serializers.flower import FlowerRequest, PatchFlowerRequest
from app.api.serializers.cart import CartFlowerRequest
from app.api.serializers.purchase import PurchaseResponse

from app.db.models import Flower


class FlowersRepository:
    @staticmethod
    def add_flower(db: Session, flower: FlowerRequest) -> int:
        db_flower = Flower(name=flower.name, count=flower.count, cost=flower.cost)
        try:
            db.add(db_flower)
            db.commit()
            db.refresh(db_flower)
        
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="Invalid flower data")
        
        return db_flower.id
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Flower]:
        return db.query(Flower).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_item(db: Session, items) -> List[CartFlowerRequest]:
        flowers = db.query(Flower).filter(Flower.id.in_(items)).all()
        return [CartFlowerRequest(id=flower.id, name=flower.name, cost=flower.cost) for flower in flowers]

    @staticmethod
    def get_by_purchase(db: Session, flower_id: int) -> List[PurchaseResponse]:
        db_flowers = db.query(Flower).filter(Flower.id == flower_id).all()
        return [PurchaseResponse(name=flower.name, cost=flower.cost) for flower in db_flowers]

    @staticmethod
    def update_flower(db: Session, flower_id: int, flower_data: PatchFlowerRequest) -> Flower:
        db_flower = db.query(Flower).filter(Flower.id == flower_id).first()
        
        if db_flower is None:
            raise HTTPException(status_code=404, detail="Flower not found")
        
        for key, value in flower_data.model_dump(exclude_unset=True).items():
            setattr(db_flower, key, value)
            
        try:
            db.commit()
            db.refresh(db_flower)
            return db_flower
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="Invalid flower data")
    
    @staticmethod 
    def delete_flower(db: Session, flower_id: int):
        db_flower = db.query(Flower).filter(Flower.id == flower_id).first()
        if db_flower is None:
            raise HTTPException(status_code=404, detail="Flower not found")
        db.delete(db_flower)
        db.commit()
        return {"message": f"Flower with id {flower_id} deleted"}
