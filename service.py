from database import get_db_connection
from models import UserCreate, UserResponse



async def create_user(user: UserCreate) -> None:

    async with get_db_connection() as conn:
        async with conn.cursor() as cursor:
            query = """ 
            INSERT INTO users (name, email, age)
            values ( %s, %s, %s)
            """

            await cursor.execute(query, (user.name, user.email, user.age))