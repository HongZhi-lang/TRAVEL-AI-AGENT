from datetime import datetime
import os
from pathlib import Path
import uuid

from dotenv import load_dotenv
from sqlalchemy import Column, DateTime, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 从 backend/.env 加载本地开发配置，确保脚本直接运行时也能读取项目环境变量。
load_dotenv(Path(__file__).resolve().parents[2] / ".env")

# 创建基类
Base = declarative_base()

# 优先使用环境变量，未设置时回退到本地默认值
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:admin123@localhost:5433/travelai")

# 打印确认
print(f"使用数据库: {DATABASE_URL}")

# 创建引擎
engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={
        "connect_timeout": 10,
        "keepalives_idle": 60,
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 基础模型类
class BaseModel(Base):
    __abstract__ = True
    
    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """转换为字典"""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }