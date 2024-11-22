import socket
import pickle

import cv2

FRAME_BUFFER = 1000000

SERVER_IP = "127.0.0.1"
SERVER_PORT = 3333

skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
skt.bind((SERVER_IP, SERVER_PORT))

while True:
    data, addr = skt.recvfrom(FRAME_BUFFER)
    frame = pickle.loads(data)

    print(f"Received frame from {addr}")

    image = cv2.imdecode(frame, cv2.IMREAD_COLOR)

    cv2.imshow("Server image", image)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
skt.close()
