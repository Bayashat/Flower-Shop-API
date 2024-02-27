from typing import List
from fastapi import HTTPException

from sqlite3 import IntegrityError
from sqlalchemy.orm import Session

from app.db.models import Cart



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
        
