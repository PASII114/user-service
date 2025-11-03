import aiomysql

from database import get_db_connection
from models import UserCreate, UserResponse



async def create_user(user: UserCreate) -> UserResponse:

    async with get_db_connection() as conn:
        async with conn.cursor() as cursor:
            query = """ 
            INSERT INTO users (name, email, age)
            values ( %s, %s, %s)
            """

            await cursor.execute(query, (user.name, user.email, user.age))
            user_id = cursor.lastrowid #getting the row id which is the user id

            async with conn.cursor(aiomysql.DictCursor) as fetch_cursor: #return the result from database as a dictionary
                query = "SELECT * FROM users WHERE id = %s"
                await fetch_cursor.execute(query, (user_id, ))
                result = await fetch_cursor.fetchone() #{'id' : 1, 'name' : 'test}

                return UserResponse(
                    id=result['id'],
                    name=result['name'],
                    email=result['email'],
                    age=result['age'],
                    created_at=result['created_at'],
                    updated_at=result['updated_at']
                )

async def get_user_by_email(email: str) -> UserResponse:

    async with get_db_connection() as conn:
        async with conn.cursor(aiomysql.DictCursor) as fetch_cursor:
            query = "SELECT * FROM users WHERE email = %s"
            await fetch_cursor.execute(query, (email, ))
            result = await fetch_cursor.fetchone()  # {'id' : 1, 'name' : 'test}

            return UserResponse(
                id=result['id'],
                name=result['name'],
                email=result['email'],
                age=result['age'],
                created_at=result['created_at'],
                updated_at=result['updated_at']
            )hi