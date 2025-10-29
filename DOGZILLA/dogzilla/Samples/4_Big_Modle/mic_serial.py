import serial
import threading
import time


class SerialPort:
    def __init__(self, port, baudrate=115200, timeout=1):

        self.ser = None
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.running = False
        self.xiaoya = False

    def open(self):
        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout
            )
            if self.ser.is_open:
                print(f"serial {self.port} open")
                self.running = True
        except Exception as e:
            print(f"open serial fail: {e}")

    def close(self):
        if self.ser and self.ser.is_open:
            self.running = False
            self.ser.close()
            print(f"serial {self.port} close")

    def send_data(self, data):
        if self.ser and self.ser.is_open:
            try:
                self.ser.write(data.encode('utf-8')) 
            except Exception as e:
                print(f"send fial: {e}")

    def clean_asr(self):
        if self.xiaoya == True:
            self.xiaoya = False

    def receive_data(self):
        global xiaoya
        step = 1
        while self.running:
            if self.ser and self.ser.is_open:
                try:
                    data = self.ser.read() 
                    if data:
                        dealdata = bytearray(data)[0]
                        if dealdata == 0xAA and step ==1:
                            step = 2
                        elif dealdata == 0x55 and step ==2:
                            step = 3
                        elif (dealdata == 0x01 or dealdata == 0x02 or dealdata == 0x03 or dealdata == 0x04 or dealdata == 0x05 or dealdata == 0x06) and step ==3:
                            step = 4
                        elif dealdata == 0x00 and step ==4:
                            step = 5
                        elif dealdata == 0xFB and step ==5:
                            self.xiaoya = True
                            step = 1

                except Exception as e:
                    print(f"recvice fail: {e}")
            time.sleep(0.1)




def main():
    port_name = "COM6"        # Windows示例
    # port_name = "/dev/ttyUSB0"  # Linux示例
    
    # 创建串口对象
    serial_port = SerialPort(port=port_name, baudrate=115200)
    serial_port.open()

    if not serial_port.ser or not serial_port.ser.is_open:
        return
    
    receive_thread = threading.Thread(target=serial_port.receive_data)
    receive_thread.daemon = True
    receive_thread.start()

    try:
        while True:
            if serial_port.xiaoya == True:
                print("唤醒成功")
                serial_port.clean_asr()

    except KeyboardInterrupt:
        pass
    finally:
        serial_port.close()

# if __name__ == "__main__":
#     main()