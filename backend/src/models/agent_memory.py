from sqlalchemy import Column, String, Text, JSON, ForeignKey, Float
from sqlalchemy.orm import relationship
from .base import BaseModel

class AgentMemory(BaseModel):
    """存储Agent的对话历史和上下文"""
    __tablename__ = "agent_memories"
    
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    trip_id = Column(String(36), ForeignKey("trips.id", ondelete="CASCADE"), nullable=True)
    
    # 对话内容
    role = Column(String(50), nullable=False)  # user, assistant, system
    content = Column(Text, nullable=False)
    
    # Agent状态
    agent_state = Column(JSON, default={})  # 保存Agent当前状态
    confidence_score = Column(Float, default=0.0)  # 置信度
    
    # 元数据
    extra_data = Column(JSON, default={})
    
    # 关联关系
    user = relationship("User", back_populates="memories")