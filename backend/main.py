from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

# >>> routers
from src.users import user_router
from src.auto import auto_router


app = FastAPI()

app.include_router(auto_router, prefix="/auto",)
app.include_router(user_router, prefix="/user",)

# if "__main__" == __name__:
