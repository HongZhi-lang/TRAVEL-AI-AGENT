from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import agent_routes
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI(
    title="Travel AI Agent API",
    description="AI驱动的智能旅行规划助手",
    version="0.1.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(agent_routes.router)

@app.get("/")
async def root():
    return {
        "message": "Travel AI Agent API is running",
        "docs": "/docs",
        "websocket": "ws://localhost:8000/api/agent/ws/chat"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "travel-ai-agent",
        "version": "0.1.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)