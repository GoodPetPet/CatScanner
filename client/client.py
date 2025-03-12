import asyncio
import websockets
import json
import logging
from aiortc import RTCPeerConnection, RTCSessionDescription,RTCIceCandidate

import logging
logger = logging.getLogger(__name__)  # __name__ 作为日志名称
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
logger.addHandler(console_handler)

# 连接到信令服务器
SIGNALING_SERVER = "ws://10.10.0.85:8080/ws?id=1"

async def signaling_client():
    # WebRTC 连接
    peer_connection = RTCPeerConnection()
    # 设置 ICE 服务器（局域网可不使用）
    peer_connection.iceServers = []
    peer_connection.iceTransportPolicy = "all"

    # 创建 DataChannel 进行数据传输
    data_channel = peer_connection.createDataChannel("chat")
    
    async with websockets.connect(SIGNALING_SERVER) as websocket:
        logger.info("connected to signaling server")

        #监听ICE
        @data_channel.on("message")
        def on_message(message):
            logger.info(f"📨 Received: {message}")

        @data_channel.on("open")
        def on_open():
            print("DataChannel opened, sending message...")
            data_channel.send("Hello, client")

        @peer_connection.on("iceconnectionstatechange")
        def on_ice_state_change():
            print(f"🌍 ICE Connection State: {peer_connection.iceConnectionState}")

        # @peer_connection.on("icecandidate")
        # async def on_ice_candidate(candidate):
        #     if candidate:
        #         print(f"❄️ Sending ICE Candidate: {candidate}")
        #         await websocket.send(json.dumps({"target":"hello","type": "candidate", "candidate": candidate.to_dict()}))
                # 监听 DataChannel 消息
        # 生成 SDP Offer
        offer = await peer_connection.createOffer()
        await peer_connection.setLocalDescription(offer)
        print(f"✅ ICE Gathering State: {peer_connection.iceGatheringState}")
        # 发送 SDP Offer
        await websocket.send(json.dumps({"target":"hello","sdp": offer.sdp, "type": offer.type}))
        logger.info("📡 Sent SDP Offer")

        while True:
            try:
                response = await websocket.recv()
                if not response:
                    logger.info("Received empty message")
                    continue
                try:
                    message = json.loads(response)
                except json.JSONDecodeError as e:
                    logger.info(f"JSON 解析失败: {e}, 收到的原始数据: {response}")
                    continue  # 跳过当前循环，继续监听消息

                if "type" in message and message["type"] == "answer":
                    # 设置远程 SDP
                    await peer_connection.setRemoteDescription(RTCSessionDescription(sdp=message['sdp'], type=message['type']))
                    logger.info("✅ Received SDP Answer")
                    if data_channel.readyState == "open":
                        print("DataChannel opened, sending message...")
                        data_channel.send("Hello after SDP Answer!")

                elif "type" in message and message["type"] == "ice-candidate":
                    # 添加 ICE Candidate
                    candidate = message["candidate"]
                    await peer_connection.addIceCandidate(candidate)
                    logger.info("📡 Added ICE Candidate")
            except websockets.exceptions.ConnectionClosed as e:
                logger.info(f"WebSocket 连接关闭: {e}")
                break  # 退出循环

logger.info("starting signaling client")
# asyncio.run(signaling_client())


async def client():
    async with websockets.connect(SIGNALING_SERVER) as ws:
        logger.info("connected to signaling server")
    pc = RTCPeerConnection()

asyncio.run(client())
