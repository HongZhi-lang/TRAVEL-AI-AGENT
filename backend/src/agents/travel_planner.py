from typing import Dict, Any, List, AsyncGenerator
import json
import logging
from .base_agent import BaseAgent
from src.services.llm_service import llm_service

logger = logging.getLogger(__name__)

class TravelPlannerAgent(BaseAgent):
    """旅行规划Agent"""
    
    def __init__(self):
        super().__init__(name="TravelPlanner")
        
    def get_system_prompt(self) -> str:
        return """
        你是一个专业的旅行规划助手。你的职责是：
        1. 根据用户需求制定详细的旅行计划
        2. 推荐合适的景点、住宿和餐饮
        3. 合理分配预算和时间
        4. 考虑天气、交通等实际因素
        
        请以友好、专业的态度与用户交流。
        如果用户需求不明确，主动询问补充信息。
        回答要具体、实用，提供可操作的建议。
        """
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理旅行规划请求
        """
        try:
            user_message = input_data.get("message", "")
            user_preferences = input_data.get("preferences", {})
            
            if not user_message:
                return {
                    "success": False,
                    "error": "消息内容不能为空"
                }
            
            # 添加到历史
            self.add_to_history("user", user_message)
            
            # 构建提示词
            messages = self.get_conversation_for_api()
            
            # 如果用户有偏好设置，添加到上下文
            if user_preferences:
                pref_prompt = f"用户偏好：{json.dumps(user_preferences, ensure_ascii=False)}"
                messages.append({"role": "user", "content": pref_prompt})
            
            # 调用LLM - 使用同步方法避免异步生成器问题
            logger.info(f"Calling LLM for message: {user_message[:50]}...")
            
            try:
                # 使用同步方法
                full_response = llm_service.chat_completion(messages)
                
                # 添加到历史
                self.add_to_history("assistant", full_response)
                
                # 尝试解析结构化信息
                structured_info = await self._extract_trip_info(full_response)
                
                return {
                    "success": True,
                    "response": full_response,
                    "structured_info": structured_info,
                    "agent_state": self.state
                }
                
            except Exception as e:
                logger.error(f"LLM调用失败: {e}")
                return {
                    "success": False,
                    "error": f"AI服务调用失败: {str(e)}"
                }
            
        except Exception as e:
            logger.error(f"TravelPlannerAgent error: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e)
            }
    
    async def process_stream(self, input_data: Dict[str, Any]) -> AsyncGenerator[str, None]:
        """
        流式处理旅行规划请求
        """
        try:
            user_message = input_data.get("message", "")
            user_preferences = input_data.get("preferences", {})
            
            if not user_message:
                yield json.dumps({
                    "type": "error",
                    "content": "消息内容不能为空"
                })
                return
            
            # 添加到历史
            self.add_to_history("user", user_message)
            
            # 构建提示词
            messages = self.get_conversation_for_api()
            
            if user_preferences:
                pref_prompt = f"用户偏好：{json.dumps(user_preferences, ensure_ascii=False)}"
                messages.append({"role": "user", "content": pref_prompt})
            
            logger.info(f"Streaming response for: {user_message[:50]}...")
            
            # 流式调用
            full_response = ""
            try:
                async for chunk in llm_service.chat_completion_stream(messages):
                    full_response += chunk
                    yield json.dumps({
                        "type": "chunk",
                        "content": chunk
                    })
                
                # 完成
                self.add_to_history("assistant", full_response)
                
                # 尝试解析结构化信息
                structured_info = await self._extract_trip_info(full_response)
                
                yield json.dumps({
                    "type": "complete",
                    "full_response": full_response,
                    "structured_info": structured_info
                })
                
            except Exception as e:
                logger.error(f"Stream error: {e}")
                yield json.dumps({
                    "type": "error",
                    "content": f"流式响应失败: {str(e)}"
                })
                
        except Exception as e:
            logger.error(f"TravelPlannerAgent stream error: {e}", exc_info=True)
            yield json.dumps({
                "type": "error",
                "content": str(e)
            })
    
    async def _extract_trip_info(self, response: str) -> Dict[str, Any]:
        """从回复中提取结构化旅行信息"""
        try:
            # 使用LLM提取关键信息
            extract_prompt = """
            从以下对话中提取旅行相关信息，以JSON格式返回：
            - destination: 目的地
            - duration: 天数（数字）
            - budget: 预算（数字）
            - interests: 兴趣点（列表）
            
            如果信息不完整，返回空值。
            只返回JSON，不要有其他内容。
            """
            
            messages = [
                {"role": "system", "content": extract_prompt},
                {"role": "user", "content": response[:500]}  # 限制长度
            ]
            
            result = llm_service.get_structured_response(
                messages,
                {"destination": "", "duration": 0, "budget": 0, "interests": []}
            )
            
            return result
        except Exception as e:
            logger.warning(f"提取结构化信息失败: {e}")
            return {}
    
    async def plan_trip(self, destination: str, days: int, budget: float, preferences: Dict = None) -> Dict:
        """直接规划行程（不用对话）"""
        prompt = f"""
        请为以下旅行需求制定详细计划：
        
        目的地：{destination}
        天数：{days}天
        预算：{budget}元
        偏好：{json.dumps(preferences, ensure_ascii=False) if preferences else '无特殊偏好'}
        
        请提供：
        1. 每日行程安排（上午、下午、晚上）
        2. 推荐的酒店（3个，不同价位）
        3. 预算分配建议
        4. 注意事项和小贴士
        
        以友好的方式呈现，内容要具体实用。
        """
        
        result = await self.process({"message": prompt})
        return result