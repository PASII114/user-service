from typing import List

from fastapi import APIRouter
from starlette import status
from starlette.exceptions import HTTPException

import service
from models import UserCreate, UserResponse

router = APIRouter(prefix="/users")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    existing_user = await service.get_user_by_email(user.email)

    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

    return await service.create_user(user)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_users(limit: int = 10, offset: int = 0) -> List[UserResponse]:
    return await service.get_all_users(limit, offset)

@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: int):
    return await service.get_user_by_id(user_id)

@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user_by_id(user_id: int):
    existing_user = await service.get_user_by_id(user_id)
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Does Not Exists")

    await service.delete_user_by_id(user_id)

    return {"info" : "User Deleted Successfully", "user" : existing_user}