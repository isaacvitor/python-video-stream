import network
import pickle
import socket
import time

from camera import Camera, GrabMode, PixelFormat, FrameSize, GainCeiling

import config

# The micropython image used in this device came from
# here https://github.imc.re/cnadler86/micropython-camera-API

SSID = config.ssid
PASS = config.password

SERVER = "192.168.1.244"
PORT = 3333


JPEG_QUALITY = 50


wlan = network.WLAN(network.STA_IF)
wlan.active(True)

cam = Camera(
    pixel_format=PixelFormat.JPEG,
    frame_size=FrameSize.HD,
    jpeg_quality=JPEG_QUALITY,
    fb_count=2,
    grab_mode=GrabMode.WHEN_EMPTY,
)

cam.init()


def do_connect():
    import network

    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        print("connecting to network...")
        wlan.active(True)
        wlan.connect(SSID, PASS)
        while not wlan.isconnected():
            pass
    print("network config:", wlan.ipconfig("addr4"))


def sendudp(host, port, data):
    addr_info = socket.getaddrinfo(host, port)
    addr = addr_info[0][-1]
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.sendto(data, addr)


def sendtcp(host, port, data):
    addr_info = socket.getaddrinfo(host, port)
    addr = addr_info[0][-1]
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.connect(addr)
    sock.send(data, "UTF8")
    sock.close()


try:
    do_connect()
    count = 1
    while True:
        img = cam.capture()
        print(len(img))

        buf = pickle.dumps(img, 0)

        # sendtcp(SERVER, PORT, buf)
        sendudp(SERVER, PORT, img)
        time.sleep(0.01)


except Exception as e:
    print(e)
finally:
    # import mip
    # mip.install("pickle")
    wlan.disconnect()
