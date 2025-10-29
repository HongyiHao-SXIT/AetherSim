#coding=utf-8
import socket
import os
import time
import threading
from DOGZILLALib import DOGZILLA
g_dog = DOGZILLA()


g_end = False

# 获取本机IP
# Read the local IP address
def getLocalIP():
    ip = os.popen(
        "/sbin/ifconfig eth0 | grep 'inet' | awk '{print $2}'").read()
    ip = ip[0: ip.find('\n')]
    if(ip == '' or len(ip) > 15):
        ip = os.popen(
            "/sbin/ifconfig wlan0 | grep 'inet' | awk '{print $2}'").read()
        ip = ip[0: ip.find('\n')]
        if(ip == ''):
            ip = 'x.x.x.x'
    if len(ip) > 15:
        ip = 'x.x.x.x'
    return ip


# 将十六进制字符串转化成整型数。  Converts a hexadecimal string to an integer.
# str_hex只支持两位字符串（一个字节数据）。 str_hex supports only two-digit strings (one byte of data).
# HEX=True表示返回无符号整型, HEX=False表示返回带符号整型。 HEX=True: returns an unsigned integer. HEX=False: returns a signed integer
def hex2int(str_hex, HEX=True):
    num_hex = int(str_hex, 16)
    if HEX:
        return num_hex
    if num_hex > 127:
        num_hex = num_hex - 256
    return num_hex
    

# 解析协议数据  Parsing protocol data
def Analysis(cmd):
    print(cmd)
    try :
        if len(cmd) == 26:
            angle = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
            for i in range(12):
                tmp = cmd[i*2+1:i*2+3]
                angle[i] = hex2int(tmp, False)
            print("read angle:", angle)
            motor_id = [11, 12, 13, 21, 22, 23, 31, 32, 33, 41, 42, 43]
            g_dog.motor(motor_id, angle)
        else:
            print("cmd len error! continue...")
    except:
        print("--- Analysis except ---")

#socket TCP通信建立 Communication to establish
def start_tcp_server(ip, port):
    global g_end
    print('start_tcp_server')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((ip, port))
    sock.listen(1)
    try:
        while True:
            my_socket, address = sock.accept()
            print("client connected:" + str(address))
            while True:
                cmd = my_socket.recv(1024).decode(encoding="utf-8") 
                if not cmd:
                    print("Client Disconnected!")
                    break
                # print('   [-]cmd:', cmd, len(cmd))
                index1 = cmd.rfind("$")
                index2 = cmd.rfind("#")
                if index1 >= 0 and index2 > index1:
                    Analysis(cmd[index1:index2+1])
            my_socket.close()
    except:
        my_socket.close()
        g_end = True


if __name__ == '__main__':
    try:
        port = 6100
        g_dog.motor_speed(50)
        while(True):
            ip = getLocalIP()
            # ip = '192.168.2.82'
            print("%s:%d" % (ip, port))
            if(ip == "x.x.x.x"):
                continue
            if(ip != "x.x.x.x"):
                break
        task_tcp = threading.Thread(target=start_tcp_server, name="task_tcp", args=(ip, port))
        task_tcp.setDaemon(True)
        task_tcp.start()
        while True:
            if g_end:
                break
            time.sleep(1)
    except KeyboardInterrupt:
        g_dog.action(0xff)
        del g_dog
        print(" Program closed! ")
        