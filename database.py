import os
from typing import Dict

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