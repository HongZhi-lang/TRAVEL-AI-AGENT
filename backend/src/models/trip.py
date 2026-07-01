from sqlalchemy import Column, String, Date, Float, Integer, JSON, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import BaseModel

class Trip(BaseModel):
    __tablename__ = "trips"
    
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # 基本信息
    title = Column(String(255), nullable=False)
    destination = Column(String(255), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    total_budget = Column(Float, nullable=False)
    
    # 行程状态
    status = Column(String(50), default="planning")  # planning, confirmed, completed, cancelled
    
    # 详细数据（JSON存储）
    daily_plan = Column(JSON, default={})  # 每日行程安排
    hotel_recommendations = Column(JSON, default=[])  # 酒店推荐
    flight_info = Column(JSON, default={})  # 航班信息
    notes = Column(Text, default="")
    
    # 关联关系
    user = relationship("User", back_populates="trips")
    
    def get_total_days(self):
        """计算旅行天数"""
        return (self.end_date - self.start_date).days + 1
    
    def to_dict(self):
        data = super().to_dict()
        data['total_days'] = self.get_total_days()
        return data