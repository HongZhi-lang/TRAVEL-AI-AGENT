from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from typing import Dict, Any
import json
from src.agents.travel_planner import TravelPlannerAgent
from src.services.llm_service import llm_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/agent", tags=["agent"])

# 全局Agent实例
travel_agent = TravelPlannerAgent()

@router.post("/chat")
async def chat_with_agent(request: Dict[str, Any]):
    """与Agent对话"""
    try:
        message = request.get("message", "")
        preferences = request.get("preferences", {})
        
        if not message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        result = await travel_agent.process({
            "message": message,
            "preferences": preferences
        })
        
        return result
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/plan")
async def create_trip_plan(request: Dict[str, Any]):
    """创建旅行计划"""
    try:
        destination = request.get("destination")
        days = request.get("days")
        budget = request.get("budget")
        preferences = request.get("preferences", {})
        
        if not all([destination, days, budget]):
            raise HTTPException(status_code=400, detail="Missing required fields")
        
        result = await travel_agent.plan_trip(destination, days, budget, preferences)
        return result
    except Exception as e:
        logger.error(f"Plan creation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """WebSocket实时对话"""
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_text()
            request = json.loads(data)
            
            message = request.get("message", "")
            preferences = request.get("preferences", {})
            
            # 处理消息
            result = await travel_agent.process({
                "message": message,
                "preferences": preferences
            })
            
            if result.get("success"):
                # 流式发送响应
                response = result.get("response", "")
                await websocket.send_text(json.dumps({
                    "type": "response",
                    "content": response,
                    "structured_info": result.get("structured_info", {})
                }))
            else:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "content": result.get("error", "Unknown error")
                }))
                
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")