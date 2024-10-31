from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

# >>> routers
from services import WSRouter
from src.users import user_router
from src.auto import auto_router
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
app.include_router(WSRouter, prefix="/ws",)

# if "__main__" == __name__:
