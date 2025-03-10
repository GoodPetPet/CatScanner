import asyncio
import websockets
import json

async def websocket_client():
    uri = "ws://localhost:8080/ws?id=2"  # 修改为你的 WebSocket 服务器地址
    try:
        async with websockets.connect(uri) as websocket:
            # 发送消息
            data = {"message":"hello world","hello server":"test","target":"peerB"}

            await websocket.send(json.dumps(data))
            print("Client: Sent message to server")

            # 接收服务器消息
            response = await websocket.recv()
            print(f"Client: Received from server -> {response}")

    except Exception as e:
        print(f"Error: {e}")

# 运行 WebSocket 客户端
asyncio.run(websocket_client())
