from fastapi import Depends, APIRouter, Response
from typing import List

from sqlalchemy.orm import Session

from app.api.serializers.cart import CartItemInput, CartItemsResponse
from app.db.models import Flower
from app.api.repositories.flowers import FlowersRepository
from app.api.repositories.carts import CartRepository
from .auth import oath2_scheme, get_db, decode_jwt


router = APIRouter()
flowers_repository = FlowersRepository()
cart_repository = CartRepository()

@router.post("/items")
def post_cart(item: CartItemInput, token: str = Depends(oath2_scheme), db: Session = Depends(get_db)):
    user_id = int(decode_jwt(token))
    cart_repository.add_to_cart(db, user_id, item.flower_id)
    return Response(status_code=201, content="Item added to cart")
    
    
@router.get("/items", response_model=CartItemsResponse)
def get_cart(token: str = Depends(oath2_scheme), db: Session = Depends(get_db)):
    user_id = int(decode_jwt(token))
    cart = cart_repository.get_cart(db, user_id)
    
    # Extract the flower_id list in the shopping cart
    flower_ids = [cart_item.flower_id for cart_item in cart]
    
    # Get the list of Flower objects corresponding to flower_id in the shopping cart
    flowers: list[Flower] = flowers_repository.get_by_item(db, flower_ids)
    
    total_cost = sum([flower.cost for flower in flowers])

    return CartItemsResponse(flowers=flowers, total_cost=total_cost)