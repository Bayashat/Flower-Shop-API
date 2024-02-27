from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.security import OAuth2PasswordBearer
from PIL import Image
from io import BytesIO

from base64 import b64encode

from sqlalchemy.orm import Session
from app.models.user import ProfileResponse
from app.db.repositories import UsersRepository
from .auth import decode_jwt, get_db

router = APIRouter()
users_repository = UsersRepository()
oath2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.get("/profile", response_model=ProfileResponse)
def get_profile(
    token: str = Depends(oath2_scheme),
    db: Session = Depends(get_db)
):
    user_id = decode_jwt(token)
    db_user = users_repository.get_by_id(db=db, id=int(user_id))
    
    
    # Get user avatar data
    photo_base64 = None
    if db_user.photo:
        photo_base64 = b64encode(db_user.photo).decode('utf-8')
        
    return ProfileResponse(
        id=db_user.id,
        email=db_user.email,
        full_name=db_user.full_name,
        photo=photo_base64,
    )
    
@router.get("/photo/{user_id}")
def get_user_photo(
    user_id: int,
    token: str = Depends(oath2_scheme),
    db: Session = Depends(get_db),
):
    user = users_repository.get_by_id(db, user_id)
    if not user or not user.photo:
        raise HTTPException(status_code=404, detail="User or photo not found")

    return StreamingResponse(BytesIO(user.photo), media_type="image/png")