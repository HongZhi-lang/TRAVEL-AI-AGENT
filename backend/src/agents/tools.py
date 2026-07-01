from typing import Dict, Any
import random
import json

class AgentTools:
    """Agent可用的工具函数"""
    
    @staticmethod
    def generate_daily_plan(destination: str, days: int, interests: List[str]) -> Dict:
        """生成每日行程"""
        # 模拟数据，实际应该调用API
        activities = {
            "文化": ["博物馆", "历史遗址", "艺术展览"],
            "自然": ["公园", "海滩", "山区"],
            "美食": ["特色餐厅", "美食街", "烹饪课程"],
            "购物": ["购物中心", "特色市场", "精品店"]
        }
        
        daily_plan = {}
        for day in range(1, days + 1):
            daily_plan[f"day_{day}"] = {
                "morning": random.choice(activities.get("文化", ["观光"])),
                "afternoon": random.choice(activities.get("自然", ["休闲"])),
                "evening": random.choice(activities.get("美食", ["用餐"]))
            }
        
        return daily_plan
    
    @staticmethod
    def estimate_cost(destination: str, days: int, budget: float) -> Dict:
        """估算费用分配"""
        return {
            "accommodation": budget * 0.4,
            "food": budget * 0.25,
            "transport": budget * 0.2,
            "activities": budget * 0.1,
            "misc": budget * 0.05
        }
    
    @staticmethod
    def validate_budget(budget: float, destination: str) -> Dict:
        """验证预算是否合理"""
        min_budget = 300 * 7  # 假设最低每日300元
        max_budget = 2000 * 7  # 假设最高每日2000元
        
        if budget < min_budget:
            return {
                "valid": False,
                "message": f"预算过低，{destination}的每日最低预算约{min_budget//7}元"
            }
        elif budget > max_budget:
            return {
                "valid": True,
                "message": "预算充足，可以享受高品质旅行"
            }
        else:
            return {
                "valid": True,
                "message": "预算合理，可以规划不错的行程"
            }