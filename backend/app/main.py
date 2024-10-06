from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.src.auto.auto_service import AutoUser
from app.src.users.user_service import UserService
from .src.users.user_controler import router as user_router
from .src.application import Access


# if "__main__" == __name__:
app = FastAPI()


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await UserService.authenticate(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = AutoUser.create_token(user)
    return {"access_token": token, "token_type": "bearer"}


app.include_router(user_router)
