from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """Agent基类"""
    
    def __init__(self, name: str, model: str = "deepseek-chat"):
        self.name = name
        self.model = model
        self.conversation_history: List[Dict] = []
        self.state: Dict[str, Any] = {}
        
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """处理输入并返回结果"""
        pass
    
    def add_to_history(self, role: str, content: str):
        """添加对话历史"""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def get_system_prompt(self) -> str:
        """获取系统提示词 - 子类重写"""
        return "你是一个有用的AI助手。"
    
    def get_conversation_for_api(self) -> List[Dict]:
        """准备对话历史用于API调用"""
        messages = [
            {"role": "system", "content": self.get_system_prompt()}
        ]
        
        # 添加最近的10条对话
        recent_history = self.conversation_history[-10:] if self.conversation_history else []
        for msg in recent_history:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        return messages