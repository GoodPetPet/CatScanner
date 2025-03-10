#!/usr/bin/env python3
import sys
import signal
import os
import numpy as np
import cv2
import colorsys
from time import time,sleep
import multiprocessing
from threading import BoundedSemaphore
import ctypes
import json
# Camera API libs

from hobot_vio import libsrcampy as srcampy
from hobot_dnn import pyeasy_dnn as dnn
import threading

is_stop=False

def signal_handler(signal, frame):
    global is_stop
    print("Stopping!\n")
    is_stop=True
    sys.exit(0)


# sensor 
sensor_width = 1920 
sensor_height = 1080
#获取输出屏幕的大小
def get_display_res():
    disp_w_small=1920
    disp_h_small=1080
    disp = srcampy.Display()
    resolution_list = disp.get_display_res()
    if (sensor_width, sensor_height) in resolution_list:
        print(f"Resolution {sensor_width}x{sensor_height} exists in the list.")
        return int(sensor_width), int(sensor_height)
    else:
        print(f"Resolution {sensor_width}x{sensor_height} does not exist in the list.")
        for res in resolution_list:
            # Exclude 0 resolution first.
            if res[0] == 0 and res[1] == 0:
                break
            else:
                disp_w_small=res[0]
                disp_h_small=res[1]

            # If the disp_w、disp_h is not set or not in the list, default to iterating to the smallest resolution for use.
            if res[0] <= sensor_width and res[1] <= sensor_height:
                print(f"Resolution {res[0]}x{res[1]}.")
                return int(res[0]), int(res[1])

    disp.close()
    return disp_w_small, disp_h_small

disp_w, disp_h = get_display_res()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    # Camera API, get camera object
    cam = srcampy.Camera()

    # Open f37 camera
    # For the meaning of parameters, please refer to the relevant documents of camera
    cam.open_cam(0, -1, -1, disp_w, disp_h,sensor_height,sensor_width)

    disp = srcampy.Display()
    # For the meaning of parameters, please refer to the relevant documents of HDMI display
    disp.display(0, disp_w, disp_h)

    # bind camera directly to display
    srcampy.bind(cam, disp)

    # change disp for bbox display
    disp.display(3, disp_w, disp_h)

    while not is_stop:
        cam_start_time = time()
        # img = cam.get_img(2, 512, 512)
        cam_finish_time = time()

    cam.close_cam()
    disp.close()
