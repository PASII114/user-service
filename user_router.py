from fastapi import APIRouter
from starlette import status

import service
from models import UserCreate

router = APIRouter(prefix="/users")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    return await service.create_user(user)