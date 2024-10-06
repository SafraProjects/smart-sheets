from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .auto_model import Token
from ..users.user_model import BaseUser


app2 = APIRouter(prefix="/aaa")


# @app2("/token", response_model=Token)
# async def login_for_access_token(user_data: BaseUser = Depends()):
#     user = authenticate_user(db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                             detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
#     access_token_expires = timedelta(minutes=Access.get_access_key())
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires)
#     return {"access_token": access_token, "token_type": "bearer"}

# return "aaaa"

# @router.get("/users/me/", response_model=User)
# async def read_users_me(current_user: User = Depends(get_current_active_user)):
#     return current_user
