from database import get_db_connection
from models import UserCreate, UserResponse



async def create_user(user: UserCreate) -> None:
