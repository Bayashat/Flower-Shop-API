from typing import List
from fastapi import HTTPException

from sqlite3 import IntegrityError
from sqlalchemy.orm import Session

from app.models.user import UserCreate
from app.models.flower import FlowerRequest, PatchFlowerRequest
from app.models.cart import CartFlowerRequest
from app.models.purchase import PurchaseResponse

from app.db.models import User, Flower, Cart, Purchase


class UsersRepository:
    def create_user(self, db: Session, user: UserCreate) -> int:
        try: 
            # Try to query if the user already exists
            existing_user = db.query(User).filter(User.email == user.email).first()
            
            if existing_user:
                raise HTTPException(status_code=400, detail="User already exists")
            
            # If the user does not exist, create a new user object and add it to the database
            db.add(user)
            db.commit()
            db.refresh(user)
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="User already exists")
        
        return user.id

    def get_by_email(self, db: Session, email: str) -> User:
        db_user = db.query(User).filter(User.email == email).first()
        if db_user:
            return db_user
        else:
            print(1111)
            print(db_user.email)
            raise HTTPException(status_code=404, detail="User not found")

    def get_by_id(self, db: Session, id: int) -> User:
        db_user = db.query(User).filter(User.id == id).first()
        if db_user:
            return db_user
        else:
            raise HTTPException(status_code=404, detail="User not found")
        
   
class FlowersRepository:
    flowers: list[Flower]

    def add_flower(self, db: Session, flower: FlowerRequest) -> int:
        db_flower = Flower(name=flower.name, count=flower.count, cost=flower.cost)
        try:
            db.add(db_flower)
            db.commit()
            db.refresh(db_flower)
        
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="Invalid flower data")
        
        return db_flower.id
        
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[Flower]:
        return db.query(Flower).offset(skip).limit(limit).all()
    
    def get_by_item(self, db: Session, items) -> List[CartFlowerRequest]:
        flowers = db.query(Flower).filter(Flower.id.in_(items)).all()
        return [CartFlowerRequest(id=flower.id, name=flower.name, cost=flower.cost) for flower in flowers]

    def get_by_purchase(self, db: Session, flower_id: int) -> List[PurchaseResponse]:
        db_flowers = db.query(Flower).filter(Flower.id == flower_id).all()
        return [PurchaseResponse(name=flower.name, cost=flower.cost) for flower in db_flowers]

    def update_flower(self, db: Session, flower_id: int, flower_data: PatchFlowerRequest) -> Flower:
        db_flower = db.query(Flower).filter(Flower.id == flower_id).first()
        
        if db_flower is None:
            raise HTTPException(status_code=404, detail="Flower not found")
        
        for key, value in flower_data.dict(exclude_unset=True).items():
            setattr(db_flower, key, value)
            
        try:
            db.commit()
            db.refresh(db_flower)
            return db_flower
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="Invalid flower data")
        
    def delete_flower(self, db: Session, flower_id: int):
        db_flower = db.query(Flower).filter(Flower.id == flower_id).first()
        if db_flower is None:
            raise HTTPException(status_code=404, detail="Flower not found")
        db.delete(db_flower)
        db.commit()
        return {"message": f"Flower with id {flower_id} deleted"}


class CartRepository:
    def get_cart(self, db: Session, user_id: int) -> List[Cart]:
        try:
            db_cart = db.query(Cart).filter(Cart.user_id == user_id).all()
            return db_cart
        except Exception as e:
            raise HTTPException(status_code=400, detail="Invalid cart data") from e
    
    def add_to_cart(self, db: Session, user_id: int, flower_id: int):
        db_cart = Cart(user_id=user_id, flower_id=flower_id)
        try:
            db.add(db_cart)
            db.commit()
            db.refresh(db_cart)
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="Invalid flower data")
        
    def clear_cart(self, db: Session, user_id: int):
        try:
            db.query(Cart).filter(Cart.user_id == user_id).delete()
            db.commit()
        except Exception as e:
            raise HTTPException(status_code=400, detail="Invalid cart data") from e 
        

class PurchasesRepository:        
    def get_user_purchases(self, db: Session, user_id: int) -> List[Purchase.flower_id]:
        try:
            purchases = db.query(Purchase).filter(Purchase.user_id == user_id).all()
            return [purchase.flower_id for purchase in purchases]
        except Exception as e:
            raise HTTPException(500, "Failed to fetch user purchases.")
        
        
        
        
    def add_purchases(self, db: Session, user_id: int, flower_ids: List[int]):
        try:
            if not flower_ids:
                raise HTTPException(400, "No flowers selected.")
            
            for flower_id in flower_ids:
                new_purchase = Purchase(user_id=user_id, flower_id=flower_id)
                db.add(new_purchase)
                db.commit()
                db.refresh(new_purchase)
                
        except HTTPException:
            raise
        
        except Exception as e:
            raise HTTPException(500, "Failed to add purchases.")
        
