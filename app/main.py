from fastapi import FastAPI, templating

from app.api.views import auth, carts, flowers, purchases, users

app = FastAPI()


app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(flowers.router, prefix="/flowers", tags=["flowers"])
app.include_router(carts.router, prefix="/carts", tags=["carts"])
app.include_router(purchases.router, prefix="/purchased", tags=["purchases"])


