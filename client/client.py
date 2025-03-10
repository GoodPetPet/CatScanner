import asyncio
import websockets
import json
import aiortc import RTCPeerConnection, RTCSessionDescription,RTCIceCandidate

# WebRTC 连接
peer_connection = RTCPeerConnection()

# 创建 DataChannel 进行数据传输
data_channel = peer_connection.create_data_channel("data")

# 连接到信令服务器
SIGNALING_SERVER = "ws://localhost:8080"

# async def websocket_client():
#     uri = "ws://localhost:8080/ws?id=1"  # 修改为你的 WebSocket 服务器地址
#     try:
#         async with websockets.connect(uri) as websocket:
#             # 发送消息
#             data = {"message":"hello client2","hello server":"222","target":"2"}

#             await websocket.send(json.dumps(data))
#             print("Client: Sent message to server")

#             # 接收服务器消息
#             response = await websocket.recv()
#             print(f"Client: Received from server -> {response}")

#     except Exception as e:
#         print(f"Error: {e}")

# # 运行 WebSocket 客户端
# asyncio.run(websocket_client())

async def signaling_client():
    async with websockets.connect(SIGNALING_SERVER) as websocket:
        print("connected to signaling server")

    #监听ICE 
    @peer_connection.on("icecandidate")
    async def on_ice_candidate(candidate):
        if candidate:
            message = {"type": "ice-candidate", "candidate": candidate.to_json()}
            await websocket.send(message)

            # 监听 DataChannel 连接
        @data_channel.on("open")
        def on_open():
            print("DataChannel opened, sending message...")
            data_channel.send("Hello from Python!")

        # 监听 DataChannel 消息
        @data_channel.on("message")
        def on_message(message):
            print(f"Received from Peer B: {message}")


                # 生成 SDP offer
        offer = await peer_connection.createOffer()
        await peer_connection.setLocalDescription(offer)

        # 发送 SDP offer
        await websocket.send(json.dumps({"type": "offer", "sdp": offer.sdp, "type": offer.type}))

        while True:
            response = await websocket.recv()
            message = json.loads(response)

            if message["type"] == "answer":
                # 设置远程 SDP
                await peer_connection.setRemoteDescription(RTCSessionDescription(message["sdp"], message["type"]))
                print("Received SDP answer")

            elif message["type"] == "ice-candidate":
                candidate = RTCIceCandidate(**message["candidate"])
                await peer_connection.addIceCandidate(candidate)


asyncio.run(signaling_client())
