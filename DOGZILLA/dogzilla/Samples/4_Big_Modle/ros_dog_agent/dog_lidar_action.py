import time,os,sys
import socket


#雷达导航接口 Radar navigation interface
def ROS_UDP_Client_Start(strdata = "APoint"):
    # 创建UDP套接字 Create UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 服务器地址配置 Server address configuration
    server_address = ('127.0.0.1', 5578)
    
    try:
        while True:
            message = strdata
            # 发送数据到服务器 Sending data to the server
            client_socket.sendto(message.encode(), server_address)
            #print(f"[*] 已发送消息到服务器")
            # 等待服务器响应 Waiting for server response
            try:  
                print("Waiting for the dog to reach the target point")
                response, server = client_socket.recvfrom(1024) 
                if response.decode()==strdata+"Get":
                    time.sleep(.5)
                    return
                
            except socket.timeout:
                print("response timeout")
                continue      
    finally:
        client_socket.close()

