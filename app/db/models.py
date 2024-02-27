from sqlalchemy import Column, Integer, String, Float, ForeignKey, LargeBinary

from app.db.base import Base

class IdMixin:
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    
class Cart(Base, IdMixin):
    __tablename__ = "carts"
    
    user_id = Column(Integer, ForeignKey("users.id"))
    flower_id = Column(Integer, ForeignKey("flowers.id"))


class Flower(Base, IdMixin):
    __tablename__ = "flowers"

    name = Column(String, nullable=False)
    count = Column(Integer, nullable=True, default=1)
    cost = Column(Float, nullable=False)
    

class Purchase(Base, IdMixin):
    __tablename__ = "purchases"

    user_id = Column(Integer, ForeignKey("users.id"))
    flower_id = Column(Integer, ForeignKey("flowers.id")) 
    


class User(Base, IdMixin):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    photo = Column(LargeBinary, nullable=True)