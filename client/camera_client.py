import websockets
import signal
import asyncio
import sys
import x3_pb2
import numpy as np


# Camera API libs
from hobot_vio import libsrcampy as srcampy
from hobot_dnn import pyeasy_dnn
fps = 30

import ctypes
import json

def signal_handler(signal, frame):
    sys.exit(0)


#models
def print_properties(pro):
    print("tensor type:", pro.tensor_type)
    print("data type:", pro.dtype)
    print("layout:", pro.layout)
    print("shape:", pro.shape)

models = pyeasy_dnn.load("./models/best.bin")
input_shape = (512, 512)

print_properties(models[0].inputs[0].properties)
print("--- model output properties ---")
for output in models[0].outputs:
    print_properties(output.properties)

# hal camera
# cam = srcampy.Camera()
# cam.open_cam(0, -1, fps, [512,1920], [512,1088],1080,1920)
# enc = srcampy.Encoder()
# enc.encode(0, 3, 1920, 1088)

# async def web_service(websocket, path=None):
#     while True:
#         FrameMessage = x3_pb2.FrameMessage()
#         FrameMessage.img_.height_ = 1080
#         FrameMessage.img_.width_ = 1920
#         FrameMessage.img_.type_ = "JPEG"

#         img = cam.get_img(2, 512, 512)
#         img = np.frombuffer(img, dtype=np.uint8)

#         origin_image = cam.get_img(2, 1920, 1088)
#         enc.encode_file(origin_image)
#         FrameMessage.img_.buf_ = enc.get_img()
#         FrameMessage.smart_msg_.timestamp_ = int(0)
#         prot_buf = FrameMessage.SerializeToString()

#         await websocket.send(prot_buf)

#     cam.close_cam()

# async def main():
#     # 创建 WebSocket 服务器
#     async with websockets.serve(web_service, "0.0.0.0", 8080):
#         # 阻塞事件循环
#         await asyncio.Future()  # 保持运行

# if __name__ == "__main__":
#     signal.signal(signal.SIGINT, signal_handler)
#     asyncio.run(main())