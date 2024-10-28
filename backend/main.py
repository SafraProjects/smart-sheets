from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

# >>> routers
from src.users import user_router
from src.auto import auto_router

# >> services
import services.application.app_service as App


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[App.Env.get_frontend_port()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auto_router, prefix="/auto",)
app.include_router(user_router, prefix="/user",)

# if "__main__" == __name__:
