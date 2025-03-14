import sys
import signal

import asyncio
import socketio
from aiortc import RTCPeerConnection, RTCSessionDescription,RTCIceCandidate
import logging

logger = logging.getLogger(__name__)  # __name__ 作为日志名称
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
logger.addHandler(console_handler)

SIGNALING_SERVER = "http://localhost:5000"

# 创建 Socket.IO 客户端
sio = socketio.AsyncClient()

# 创建 RTCPeerConnection 对象
pc = RTCPeerConnection()
data_channel = pc.createDataChannel("data")
        #监听ICE
@data_channel.on("message")
def on_message(message):
    logger.info(f"📨 Received: {message}")

@data_channel.on("open")
def on_open():
    print("DataChannel opened, sending message...")
    data_channel.send("Hello, client")

@sio.on('message')
async def handle_offer(data):
    if (data["type"]=="offer"):
        await pc.setRemoteDescription(RTCSessionDescription(sdp=data["offer"], type=data["type"]))

        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)

        await sio.emit("message", {"answer": pc.localDescription.sdp,"type":answer.type})
        logger.info("📡 Sent SDP Answer")

# 连接 WebSocket 服务器
@sio.event
async def connect():
    print("Connected to signaling server")
    # 注册用户
    await sio.emit("register", {"username": "userB"})
# 监听断开连接
@sio.event
async def disconnect():
    print("Disconnected from server")

def signal_handler(signal, frame):
    """ 处理 Ctrl+C (SIGINT) """
    print("\nReceived Ctrl+C, disconnecting...")
    sys.exit(0)

async def connect_to_server():
    # 连接服务器
    await sio.connect(SIGNALING_SERVER)
        # 保持连接
    await sio.wait()



if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    asyncio.run(connect_to_server())
