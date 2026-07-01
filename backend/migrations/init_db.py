import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.base import engine, Base
from src.models.user import User
from src.models.trip import Trip
from src.models.agent_memory import AgentMemory

def init_database():
    """初始化数据库表"""
    print("Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")
    except Exception as exc:
        print(f"Failed to initialize database: {exc}")
        print("Tip: set DATABASE_URL to a reachable PostgreSQL instance before rerunning this script.")
        raise

if __name__ == "__main__":
    init_database()