# backend/test_websocket.py
import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://localhost:8000/api/agent/ws/chat"
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps({
            "message": "我想去成都旅游，4天，预算5000"
        }))
        
        response = await websocket.recv()
        print(json.loads(response))

asyncio.run(test_websocket())