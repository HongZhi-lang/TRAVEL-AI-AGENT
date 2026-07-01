import json
from typing import List, Dict, Any, Optional
from openai import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from src.config.settings import settings
import logging

logger = logging.getLogger(__name__)

class LLMService:
    """DeepSeek LLM服务封装"""
    
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.DEEPSEEK_API_KEY,
            base_url=settings.DEEPSEEK_BASE_URL
        )
        
        # LangChain兼容接口
        self.langchain_llm = ChatOpenAI(
            model=settings.DEEPSEEK_MODEL,
            openai_api_key=settings.DEEPSEEK_API_KEY,
            openai_api_base=settings.DEEPSEEK_BASE_URL,
            temperature=0.7,
        )
    
    def chat_completion(self, messages: List[Dict], temperature: float = 0.7) -> str:
        """
        同步聊天完成
        """
        try:
            response = self.client.chat.completions.create(
                model=settings.DEEPSEEK_MODEL,
                messages=messages,
                temperature=temperature,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"DeepSeek API error: {e}")
            raise
    
    async def chat_completion_stream(self, messages: List[Dict], temperature: float = 0.7):
        """
        流式聊天完成
        """
        try:
            stream = self.client.chat.completions.create(
                model=settings.DEEPSEEK_MODEL,
                messages=messages,
                temperature=temperature,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            logger.error(f"DeepSeek stream error: {e}")
            raise
    
    def get_structured_response(self, messages: List[Dict], response_format: Dict) -> Dict:
        """
        获取结构化响应（JSON格式）
        """
        try:
            # 添加格式要求
            system_msg = {
                "role": "system",
                "content": f"请以JSON格式返回结果，格式为: {json.dumps(response_format)}"
            }
            
            messages_with_format = [system_msg] + messages
            
            response = self.client.chat.completions.create(
                model=settings.DEEPSEEK_MODEL,
                messages=messages_with_format,
                temperature=0.3,  # 降低温度使输出更确定
                response_format={"type": "json_object"}
            )
            
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            logger.error(f"Structured response error: {e}")
            raise

# 全局实例
llm_service = LLMService()