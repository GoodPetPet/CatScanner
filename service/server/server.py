import asyncio
import json
from json.decoder import JSONDecodeError
from aiohttp import web

# 存储 WebSocket 连接
connected_clients = {}

async def handle_websocket(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    # 获取唯一 ID
    client_id = request.query.get("id")
    if not client_id:
        await ws.close()
        return ws

    connected_clients[client_id] = ws
    print(f"Client {client_id} connected")

    async for msg in ws:
        if msg.type == web.WSMsgType.TEXT:
            try :
                data = json.loads(msg.data)
            except JSONDecodeError as e:
                print(f"解析 JSON 数据失败: {e}")
                error_response = json.dumps({"status": "error", "message": "Invalid JSON format or empty data"})
                await ws.send_json(error_response)
                continue
            
            target_id = data.get("target")
            if target_id in connected_clients:
                await connected_clients[target_id].send_json(data)
            else:
                print(f"Target {target_id} not found")
                error_response = json.dumps({"status": "error", "message": "Target {} not found".format(target_id)})
                await ws.send_json(error_response)

        elif msg.type == web.WSMsgType.ERROR:
            print(f"WebSocket error: {ws.exception()}")

    del connected_clients[client_id]
    print(f"Client {client_id} disconnected")
    return ws

app = web.Application()
app.router.add_get("/ws", handle_websocket)

if __name__ == "__main__":
    web.run_app(app, port=8080)
