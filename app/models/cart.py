from typing import List

from pydantic import BaseModel

class CartItemInput(BaseModel):
    flower_id: int
    
    
class CartFlowerRequest(BaseModel):
    id: int
    name: str
    cost: float
        

class CartItemsResponse(BaseModel):
    flowers: List[CartFlowerRequest]
    total_cost: float
