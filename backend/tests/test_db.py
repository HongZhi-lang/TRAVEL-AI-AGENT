import asyncpg
import os
from dotenv import load_dotenv
from sqlalchemy.engine import make_url

load_dotenv()

database_url = make_url(
    os.getenv("DATABASE_URL", "postgresql://admin:admin123@localhost:5433/travelai")
)

async def test_connection():
    try:
        conn = await asyncpg.connect(
            user=database_url.username,
            password=database_url.password,
            database=database_url.database,
            host=database_url.host,
            port=database_url.port
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