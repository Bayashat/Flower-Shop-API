from typing import List
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.db.models import Purchase

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
        
