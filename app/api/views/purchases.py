from fastapi import Depends, APIRouter, Response
from typing import List, Any

from sqlalchemy.orm import Session

from app.models.purchase import PurchaseResponse
from app.db.repositories import FlowersRepository, CartRepository, PurchasesRepository
from .auth import oath2_scheme, get_db, decode_jwt


router = APIRouter()
flowers_repository = FlowersRepository()
cart_repository = CartRepository()
purchases_repository = PurchasesRepository()


@router.get("/", response_model=List[PurchaseResponse])
def get_purchased(token: str = Depends(oath2_scheme), db: Session = Depends(get_db)) -> Any:
    # parse token to get user info
    user_id = decode_jwt(token)
    
    # get user's purchases(flower ids)
    purchased_flower_ids = purchases_repository.get_user_purchases(db, user_id)
    
    # get correcponding flowers
    purchased_flowers: List[PurchaseResponse] = flowers_repository.get_by_item(db, purchased_flower_ids)

    return purchased_flowers


@router.post("/")
def post_purchased(token: str = Depends(oath2_scheme), db: Session = Depends(get_db)):
    # parse token to get user info
    user_id = int(decode_jwt(token))
    
    cart = cart_repository.get_cart(db, user_id)
    
    cart_flower_ids = [item.flower_id for item in cart]
        
    purchases_repository.add_purchases(db, user_id, cart_flower_ids)
    
    # Clear the cart after purchase
    cart_repository.clear_cart(db, user_id)
    
    return Response(status_code=201, content="Purchase successfull")

