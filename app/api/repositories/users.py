from fastapi import HTTPException

from sqlite3 import IntegrityError
from sqlalchemy.orm import Session

from app.api.serializers.user import UserCreate

from app.db.models import User


class UsersRepository:
    @staticmethod
    def create_user(db: Session, user: UserCreate) -> int:
        try: 
            # Try to query if the user already exists
            existing_user = db.query(User).filter(User.email == user.email).first()
            
            if existing_user:
                raise HTTPException(status_code=400, detail="User already exists")
            
            # If the user does not exist, create a new user object and add it to the database
            db.add(user)
            db.commit()
            db.refresh(user)
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="User already exists")
        
        return user.id

    @staticmethod
    def get_by_email(db: Session, email: str) -> User:
        db_user = db.query(User).filter(User.email == email).first()
        if db_user:
            return db_user
        else:
            raise HTTPException(status_code=404, detail="User not found")

    @staticmethod
    def get_by_id(db: Session, id: int) -> User:
        db_user = db.query(User).filter(User.id == id).first()
        if db_user:
            return db_user
        else:
            raise HTTPException(status_code=404, detail="User not found")
        
   