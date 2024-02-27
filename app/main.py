from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, templating

from app.db.repositories import UsersRepository, FlowersRepository, CartRepository, PurchasesRepository
from app.api import auth, carts, flowers, purchases, users

app = FastAPI()
templates = templating.Jinja2Templates("templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(flowers.router, prefix="/flowers", tags=["flowers"])
app.include_router(carts.router, prefix="/carts", tags=["carts"])
app.include_router(purchases.router, prefix="/purchased", tags=["purchases"])


