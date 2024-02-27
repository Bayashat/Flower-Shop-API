from jose import jwt

from fastapi import APIRouter, Form, Response, HTTPException, Depends, UploadFile, File
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session
from pydantic import EmailStr

from app.db.database import SessionLocal
from app.db.models import User
from app.models.user import ProfileResponse
from app.db.repositories import UsersRepository

router = APIRouter()
users_repository = UsersRepository()
oath2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")\
    
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png"]

# JWT part
def create_jwt(user_id: int) -> str:
    body = {"user_id": user_id}
    token = jwt.encode(body, "flower-secret", algorithm="HS256")
    return token
    
def decode_jwt(token: str) -> int:
    data = jwt.decode(token, "flower-secret", algorithms="HS256") # json
    return data["user_id"]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()

# 1.Signup
@router.post("/signup")
def post_signup(
    email: EmailStr = Form(),
    full_name: str = Form(),
    password: str = Form(),
    photo: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    user = User(email=email, full_name=full_name, password=password)
    
    if photo:
        # check file type
        if photo.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(status_code=400, detail="Invalid image type")
        
        # Read file contents in chunks
        user.photo = b"".join(chunk for chunk in iter(lambda: photo.file.read(4096), b""))
    
    user_id = users_repository.create_user(db, user)
    
    return Response(status_code=201, content=f"User {user_id} created")


# 2.Login
@router.post("/login")
def post_login(
    username: str = Form(), 
    password: str = Form(),
    db: Session = Depends(get_db)
):
    user = users_repository.get_by_email(db, username)
    
    if user.password == password:
        token = create_jwt(user.id)
        return {"access_token": token, "type": "bearer"}
    
    raise HTTPException(status_code=401, detail="Invalid password")