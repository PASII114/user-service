from contextlib import asynccontextmanager
from fileinput import close

from fastapi import FastAPI

from database import init_database, close_pool
from user_router import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_database()
    yield
    await close_pool()


app = FastAPI(
    title="User Service with Database Integration",
    lifespan=lifespan
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("App is Starting")
    await init_database()
    yield
    await close_pool()


app.include_router(router=router)