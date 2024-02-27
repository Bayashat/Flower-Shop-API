from typing import List
from pydantic import BaseModel


class FlowerResponse(BaseModel):
    id: int
    name: str
    count: int
    cost: float
 
   
class FlowerRequest(BaseModel):
    name: str
    count: int | None = None
    cost: float


class PatchFlowerRequest(BaseModel):
    name: str | None = None
    count: int | None = None
    cost: float | None = None


class FlowersResponse(BaseModel):
    data: List[FlowerResponse]
    


