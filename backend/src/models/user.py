from sqlalchemy import Column, String, Boolean, JSON
from sqlalchemy.orm import relationship
from .base import BaseModel

class User(BaseModel):
    __tablename__ = "users"
    
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    
    # 用户偏好设置（JSON存储）
    preferences = Column(JSON, default={
        "default_budget": 5000,
        "preferred_cuisine": [],
        "travel_style": "balanced",  # budget, luxury, balanced
        "interests": []
    })
    
    # 关联关系
    trips = relationship("Trip", back_populates="user", cascade="all, delete-orphan")
    memories = relationship("AgentMemory", back_populates="user", cascade="all, delete-orphan")
    
    def to_dict(self):
        data = super().to_dict()
        data.pop("hashed_password")  # 不返回密码
        return data