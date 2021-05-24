import socket
import time
from io import BytesIO

HOST = '127.0.0.1'
PORT = 65432        

BUFF_SIZE = 1024

def sendData(sock, msg):
    sock.sendall(bytes(msg, "utf8"))

def receive(sock): 
    data = b''
    while True:
        while True:
            part = sock.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                break
        if data:
            break
    return data.decode().strip()

# Đăng nhập
def login():
    u = input('Username: ')
    sendData(client, u)
    p = input('Password: ')
    sendData(client, p)
    data = receive(client)
    if (data == '1'):
        print('Đăng nhập thành công')
    elif (data == '-1'):
        print('Sai mật khẩu')
    else:
        print('Tài khoản không tồn tại')

# Đăng ký
def regist():
    u = input('Username: ')
    sendData(client, u)
    p = input('Password: ')
    sendData(client, p)
    data = receive(client)
    if (data == '1'):
        print('Đăng kí thành công')
        return True
    else:
        print('Tên đăng nhập tồn tại')
        return False

def matchDetail():
    id = input('Match ID: ')
    sendData(client, id)
    detail = receive(client)
    print(detail)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    server_address = (HOST, PORT)
    print("Client connect to server with port: " + str(PORT))
    client.connect(server_address)
    try:
        while True:
            msg = input('Client: ')
            sendData(client, msg)
            if (msg == "LOGIN"):
                msg = input('Client: ')
                sendData(client, msg)
                if (msg == "LOG"):
                    login()

            elif (msg == "REGIST"):
                while True:
                    msg = input('Client: ')
                    sendData(client, msg)
                    if (msg == "REG"):
                        check = regist()
                        if check:
                            break
                    else:
                        break
            
            elif (msg == "DETAIL"):
                while True:
                    msg = input('Client: ')
                    sendData(client, msg)
                    if (msg == "DET"):
                        matchDetail()
                    else:
                        break

            else:
                break
            
    except KeyboardInterrupt:
        client.close()
    finally:
        client.close()