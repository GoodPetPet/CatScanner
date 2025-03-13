import asyncio
import json
import websockets
from aiortc import RTCPeerConnection, RTCSessionDescription

SIGNALING_SERVER = "ws://localhost:8080/ws?id=hello"

async def signaling_client():
    peer_connection = RTCPeerConnection()

    data_channel = None  # 先定义 DataChannel

    async with websockets.connect(SIGNALING_SERVER) as websocket:
        print("✅ Connected to signaling server")
        # 监听 ICE 候选者
        @peer_connection.on("icecandidate")
        async def on_ice_candidate(candidate):
            if candidate:
                message = json.dumps({"target":"1","type": "ice-candidate", "candidate": candidate.to_json()})
                await websocket.send(message)
                print("📡 Sent ICE Candidate")

        # 监听 DataChannel
        @peer_connection.on("datachannel")
        def on_data_channel(channel):
            global data_channel
            data_channel = channel
            print("📡 DataChannel received from Client A")

            @channel.on("open")
            def on_open():
                print("📡 DataChannel Opened! Sending message...")
                channel.send("Hello from Client B!")

            @channel.on("message")
            def on_message(message):
                print(f"📨 Received from A: {message}")
        
        # 监听整体连接状态
        @peer_connection.on("connectionstatechange")
        async def on_connection_state_change():
            print(f"🔄 WebRTC Connection State: {peer_connection.connectionState}")

        @peer_connection.on("iceconnectionstatechange")
        async def on_ice_state_change():
            print(f"🔄 ICE Connection State: {peer_connection.iceConnectionState}")

        while True:
            response = await websocket.recv()
            message = json.loads(response)

            if message["type"] == "offer":

                # 设置远程 SDP
                await peer_connection.setRemoteDescription(RTCSessionDescription(message["sdp"], message["type"]))

                # 生成 SDP Answer
                answer = await peer_connection.createAnswer()
                await peer_connection.setLocalDescription(answer)
                async def wait_for_ice_gathering_complete(peer_connection):
                    while peer_connection.iceGatheringState != "complete":
                        await asyncio.sleep(0.1)  # 等待 ICE 收集完成
                    print("✅ ICE Gathering Completed")
                    return peer_connection.localDescription
                # 等待 ICE 收集完成
                final_sdp = await wait_for_ice_gathering_complete(peer_connection)
                # 发送 SDP Answer
                await websocket.send(json.dumps({"target":"1","sdp":final_sdp.sdp, "type": final_sdp.type}))
                print("✅ Sent SDP Answer")

            elif message["type"] == "ice-candidate":
                print(f"📡 Received ICE Candidate: {message['candidate']}")
                await peer_connection.addIceCandidate(message["candidate"])
                print("📡 Added ICE Candidate")

asyncio.run(signaling_client())
