import socket
import cv2
import numpy as np

#It is a server to attend to micropython clients, it doesn't work in a micropython device
FRAME_BUFFER = 1000000

SERVER_IP = "192.168.1.244"
SERVER_PORT = 3333

skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
skt.bind((SERVER_IP, SERVER_PORT))

while True:
    data, addr = skt.recvfrom(FRAME_BUFFER)
    print(f"Received frame from {addr}")
    if data:
        # frame = pickle.loads(data)
        image_arr = np.frombuffer(data, np.uint8)
        image = cv2.imdecode(image_arr, cv2.IMREAD_COLOR)

        cv2.imshow("Server image", image)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
skt.close()
