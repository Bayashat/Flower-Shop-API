from sqlalchemy import Column, Integer, String, Float, ForeignKey, LargeBinary

from app.db.base import Base


class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    flower_id = Column(Integer, ForeignKey("flowers.id"))


class Flower(Base):
    __tablename__ = "flowers"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String, nullable=False)
    count = Column(Integer, nullable=True, default=1)
    cost = Column(Float, nullable=False)
    

class Purchase(Base):
    __tablename__ = "purchases"
    
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    flower_id = Column(Integer, ForeignKey("flowers.id")) 
    


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, index=True)
    email = Column(String, unique=True, primary_key=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    photo = Column(LargeBinary, nullable=True)