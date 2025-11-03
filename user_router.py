from fastapi import APIRouter
from starlette import status

import service
from models import UserCreate

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