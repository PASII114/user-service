from typing import Optional, List

import aiomysql
from pydantic import EmailStr

from database import get_db_connection
from models import UserCreate, UserResponse, UserUpdate


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

async def get_user_by_email(email: EmailStr) -> Optional[UserResponse]:

    async with get_db_connection() as conn:
        async with conn.cursor(aiomysql.DictCursor) as fetch_cursor:
            query = "SELECT * FROM users WHERE email = %s"
            await fetch_cursor.execute(query, (email, ))
            result = await fetch_cursor.fetchone()  # {'id' : 1, 'name' : 'test}
            if result:
                return UserResponse(
                    id=result['id'],
                    name=result['name'],
                    email=result['email'],
                    age=result['age'],
                    created_at=result['created_at'],
                    updated_at=result['updated_at']
                )
            return None

async def get_all_users(limit: int, offset: int) -> List[UserResponse]:

    async with get_db_connection() as conn:
        async with conn.cursor(aiomysql.DictCursor) as fetch_cursor:
            query = "SELECT * FROM users ORDER by id LIMIT %s OFFSET %s"
            await fetch_cursor.execute(query, (limit, offset))
            results = await fetch_cursor.fetchall()  # {'id' : 1, 'name' : 'test}
            user_resp_list: List[UserResponse] = []

            if len(results) > 0:
                for result in results:
                    user = UserResponse(
                        id=result['id'],
                        name=result['name'],
                        email=result['email'],
                        age=result['age'],
                        created_at=result['created_at'],
                        updated_at=result['updated_at']
                    )
                    user_resp_list.append(user)
            return user_resp_list

async def get_user_by_id(id: int) -> Optional[UserResponse]:

    async with get_db_connection() as conn:
        async with conn.cursor(aiomysql.DictCursor) as fetch_cursor:
            query = "SELECT * FROM users WHERE id = %s"
            await fetch_cursor.execute(query, (id, ))
            result = await fetch_cursor.fetchone()  # {'id' : 1, 'name' : 'test}
            if result:
                return UserResponse(
                    id=result['id'],
                    name=result['name'],
                    email=result['email'],
                    age=result['age'],
                    created_at=result['created_at'],
                    updated_at=result['updated_at']
                )
            return None

async def delete_user_by_id(id: int):

    async with get_db_connection() as conn:
        async with conn.cursor() as delete_cursor:
            query = "DELETE FROM users WHERE id = %s"
            await delete_cursor.execute(query, (id, ))
            result = await delete_cursor.fetchone()
            if result:
                return result.pop(id)
            return None

async def replace_user(user_id, user) -> UserResponse:

    async with get_db_connection() as conn:
        async with conn.cursor() as cursor:
            query = """ 
            UPDATE users SET name = %s, email = %s, age = %s where id = %s
            """

            await cursor.execute(query, (user.name, user.email, user.age, user_id))

            return await get_user_by_id(user_id)

async def patch_user(user_id, user) -> Optional[UserResponse]:

    async with get_db_connection() as conn:
        async with conn.cursor() as cursor:
            query_string_values = []
            values = []

            if user.name:
                query_string_values.append("name = %s")
                values.append(user.name)
            if user.email:
                query_string_values.append("email = %s")
                values.append(user.email)
            if user.age:
                query_string_values.append("age = %s")
                values.append(user.age)

            if len(query_string_values) == 0:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")

            query = f"UPDATE users SET {','.join(query_string_values)}, updated_at=CURRENT_TIMESTAMP where id = %s"
            values.append(user_id)
            await cursor.execute(query, values)

            return await get_user_by_id(user_id)