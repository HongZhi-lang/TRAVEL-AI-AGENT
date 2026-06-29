import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def test_connection():
    try:
        conn = await asyncpg.connect(
            user='admin',
            password='admin123',
            database='travelai',
            host='localhost',
            port=5432
        )
        version = await conn.fetchval('SELECT version()')
        print(f"Connected to PostgreSQL: {version}")
        await conn.close()
        return True
    except Exception as e:
        print(f"Connection failed: {e}")
        return False

# 运行测试
# python -c "import asyncio; from test_db import test_connection; asyncio.run(test_connection())"