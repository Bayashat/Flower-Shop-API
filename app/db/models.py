from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, LargeBinary

from app.db.base import Base

class IdMixin:
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
   
class User(Base, IdMixin):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    photo = Column(LargeBinary, nullable=True) 
    

class Flower(Base, IdMixin):
    __tablename__ = "flowers"

    name = Column(String, nullable=False)
    count = Column(Integer, nullable=True, default=1)
    cost = Column(Numeric(precision=10, scale=2), nullable=False)    


class Cart(Base, IdMixin):
    __tablename__ = "carts"
    
    user_id = Column(Integer, ForeignKey("users.id"))
    flower_id = Column(Integer, ForeignKey("flowers.id"))


    
class Purchase(Base, IdMixin):
    __tablename__ = "purchases"

    user_id = Column(Integer, ForeignKey("users.id"))
    flower_id = Column(Integer, ForeignKey("flowers.id")) 


