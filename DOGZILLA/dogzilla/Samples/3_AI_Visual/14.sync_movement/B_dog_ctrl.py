#coding=utf-8
import socket
import os
import time
from DOGZILLALib import DOGZILLA
g_dog = DOGZILLA()

global g_sock


# 将整型十进制数转化成十六进制数。Converts an integer decimal number to a hexadecimal number.
# int_hex=[-128, 255]
def int2hex(int_hex):
    if int_hex < -128 or int_hex > 255:
        int_hex = 0
    if int_hex < 0:
        int_hex = int_hex + 256
    return int_hex

# 准备姿态并卸载一条腿 Prepare stance and unload one leg
def ctrl_Leg(leg):
    if leg == 1:
        motor_id = [11, 12, 13, 21, 22, 23, 31, 32, 33, 41, 42, 43]
        angle = [27, 48, 0, 50, 16, 0, 27, 15, 0, 27, 15, 0]
        g_dog.motor(motor_id, angle)
        time.sleep(2)
        g_dog.unload_motor(1)


# socket客户端连接服务 Socket client connection service
def connect_tcp_server(ip, port):
    global g_sock
    print("Connecting server...")
    g_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    g_sock.connect((ip, port))
    print("Connected!")
    time.sleep(.1)
    while True:
        # angle = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        angle = g_dog.read_motor(True)
        print("angle=", angle)
        if len(angle) == 12:
            for i in range(12):
                angle[i] = int2hex(angle[i])
            data = "$%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x#" % \
                (angle[0], angle[1], angle[2], angle[3], angle[4], angle[5], 
                angle[6], angle[7], angle[8], angle[9], angle[10], angle[11])
            # print(data)
            b_data = bytes(data, encoding = "utf8")
            g_sock.send(b_data)


# 关闭 close socket
def waitClose(sock):
    sock.close()



if __name__ == '__main__':
    # 根据A_DOG的IP地址修改以下参数
    # Modify the following parameters based on the IP address of A DOG
    ip = '192.168.2.112'
    port = 6100
    leg = 1
    try:
        ctrl_Leg(leg)
        connect_tcp_server(ip, port)
    except:
        g_dog.load_motor(leg)
        g_dog.action(0xff)
        waitClose(g_sock)
        del g_dog
        print(" Program closed! ")
