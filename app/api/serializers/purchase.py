from pydantic import BaseModel


class PurchaseResponse(BaseModel):
    name: str
    cost: float
    