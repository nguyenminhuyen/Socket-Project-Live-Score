import socket
import json

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

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
    usr = ""
    psw = ""
    usr = receive(conn)
    psw = receive(conn)
            
    fd = open("account.json", "r")
    userExist = False
    accs = json.loads(fd.read())
    for acc in accs["account"]:
        u = acc["usr"]
        p = acc["psw"]
        if u == usr:
            if p == psw:
                sendData(conn, '1') # Đăng nhập thành công
            else:
                sendData(conn, '-1') # Sai mật khẩu
            userExist = True
    if not userExist:
        sendData(conn, '0') # Tài khoản không tồn tại
    fd.close()

# Đăng ký
def regist():
    usr = ""
    psw = ""
    usr = receive(conn)
    psw = receive(conn)

    fd = open("account.json", "r+")
    userExist = False
    accs = json.loads(fd.read())
    for acc in accs["account"]:
        u = acc["usr"]
        if u == usr:
            sendData(conn, '0') # Tên đăng nhập đã tồn tại
            userExist = True
            return False
    if not userExist:
        accs["account"].append({"usr": usr,"psw": psw})
        accs.update(accs)
        fd.seek(0)
        json.dump(accs, fd, indent = 4)
        sendData(conn, '1') # Đăng ký thành công
    fd.close()
    return True

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        str = ""
        while True:
            str = receive(conn)
            print(str)

            if (str == "LOGIN"):
                str = receive(conn)
                if (str == "LOG"):
                    login()

            elif (str == "REGIST"):
                while True:
                    str = receive(conn)
                    if (str == "REG"):
                        flag = regist()
                        if flag:
                            break
                    else:
                        break

            else:
                break
    conn.close()