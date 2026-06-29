# Travel AI Agent - 智能旅行规划助手

[![Python Version](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14-black)](https://nextjs.org/)
[![DeepSeek](https://img.shields.io/badge/DeepSeek-API-orange)](https://deepseek.com/)

## 项目简介

基于AI Agent的智能旅行规划系统，使用DeepSeek大语言模型驱动，实现智能对话、行程规划、预算分配等功能。

## 技术栈

### 后端
- FastAPI (Python)
- PostgreSQL
- Redis (缓存 + 会话)
- WebSocket (实时进度)
- Docker Compose

### 前端
- Next.js 14 (App Router) + TypeScript
- Tailwind CSS + shadcn/ui
- Zustand (状态管理)
- React Query (数据获取)
- Vercel AI SDK (流式响应)

### AI Agent 核心
- LangChain + LangGraph (Agent框架)
- DeepSeek API
- 工具集成: 
  - 天气API (OpenWeather)
  - 地图API (Google Maps/Mapbox)
  - 酒店API (Booking.com API)
  - 航班API (Amadeus)
- Vector DB: Pinecone/Qdrant (记忆存储)
- 模型: 本地Embedding模型 (BGE)


## 📁 项目结构

```
travel-ai-agent/
├── backend/
│   ├── src/
│   │   ├── agents/      # AI Agent实现
│   │   ├── api/         # REST/WebSocket API
│   │   ├── models/      # 数据模型
│   │   ├── services/    # 业务逻辑
│   │   └── config/      # 配置管理
│   ├── migrations/      # 数据库迁移
│   ├── tests/          # 单元测试
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── app/            # Next.js页面
│   ├── components/     # React组件
│   ├── lib/           # 工具函数
│   └── package.json
├── docker/
│   └── docker-compose.yml
├── .github/           # GitHub配置
└── README.md
```

## 快速开始

### 前置条件
- Node.js 18+
- Python 3.11+
- Docker Desktop
- DeepSeek API Key

### 启动
1. 启动Docker服务: docker-compose up -d
2. 启动后端: cd backend && uvicorn src.main:app --reload
3. 启动前端: cd frontend && npm run dev
4. 访问前端: http://localhost:3000
5. 访问API文档: http://localhost:8000/docs
6. 管理数据库: http://localhost:5050

> 需要配置 env 环境变量,填入 `DEEPSEEK_API_KEY`

### 虚拟环境管理
```
# 每次打开新终端，记得激活虚拟环境
cd backend
.\venv\Scripts\Activate.ps1

# 查看已安装的包
pip list

# 导出当前环境（更新requirements.txt）
pip freeze > requirements.txt
```

## Docker 容器管理
```powershell
# 查看所有容器状态
docker ps -a

# 查看容器日志
docker logs travelai-postgres
docker logs travelai-redis

# 停止所有容器
docker-compose down

# 停止并删除所有数据（谨慎！）
docker-compose down -v

# 重新构建并启动
docker-compose up -d --build
```

## 端口冲突检查
```powershell
# 检查端口占用
netstat -ano | findstr :3000  # 前端
netstat -ano | findstr :8000  # 后端API
netstat -ano | findstr :5432  # PostgreSQL
netstat -ano | findstr :6379  # Redis
netstat -ano | findstr :5050  # pgAdmin

# 如果端口被占用，杀死进程
taskkill /PID [进程ID] /F
```

## 常见错误及解决
```powershell
# 错误：Cannot connect to the Docker daemon
# 解决：启动Docker Desktop

# 错误：Address already in use
# 解决：修改端口映射或关闭占用进程

# 错误：ModuleNotFoundError
# 解决：检查虚拟环境是否激活，重新安装依赖

# 错误：psycopg2.OperationalError
# 解决：检查PostgreSQL是否运行，连接参数是否正确
```