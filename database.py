import os
from contextlib import asynccontextmanager
from typing import Dict

import aiomysql
from dotenv import load_dotenv







load_dotenv()

DB_CONFIG : Dict[str, any] = {
    'host' : os.getenv('DB_HOST', 'localhost'),
    'port' : int(os.getenv('DB_PORT', 3306)),
    'password' : os.getenv('DB_PASSWORD', 'pass'),
    'user' : os.getenv('DB_USER', 'root'),
    'db' : os.getenv('DB_NAME', 'user_db'),
    'autocommit' : True
}

_pool: aiomysql.Pool = None

async def get_pool():
    global _pool
    if _pool is None:
        _pool = await aiomysql.create_pool(**DB_CONFIG, minsize=1, maxsize=5) # type: ignore
    return _pool

async def close_pool():
    global _pool

    if _pool:
        _pool.close()
        await _pool.wait_closed()
        _pool = None

@asynccontextmanager
async def get_db_connection():
    pool = await get_pool()
    async with pool.acquire() as conn:
        try:
            yield conn
        except Exception as e:
            await conn.rollback()
            raise e

async def init_database():
    async with get_db_connection as conn:
        async with conn.cursor() as cursor:

            user_tabel_sql = """
            
            CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name varchar(100) NOT NULL,
            email varchar(100) UNIQUE,
            age INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP
            )
            
            """

            await cursor.execute(user_tabel_sql)
