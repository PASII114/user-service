from fastapi import APIRouter
from starlette import status

import service
from models import UserCreate

router = APIRouter(prefix="/users")