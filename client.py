import socket
import pickle
import os

import cv2
import numpy as np

FRAME_BUFFER = 1000000
IMAGE_QUALITY = 80
# X_SCREEN = 640
# Y_SCREEN = 480
X_SCREEN = 1280
Y_SCREEN = 720

SERVER_IP = "127.0.0.1"
SERVER_PORT = 3000

skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
skt.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, FRAME_BUFFER)

input_video = cv2.VideoCapture(0)
input_video.set(3, X_SCREEN)
input_video.set(4, Y_SCREEN)

while input_video.isOpened():
    ret, frame = input_video.read()
    if not ret:
        break

    cv2.imshow("frame", frame)
    ret, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, IMAGE_QUALITY])

    data = pickle.dumps(buffer, 0)

    skt.sendto(data, (SERVER_IP, SERVER_PORT))

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
input_video.release()
