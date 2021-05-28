import socket
import json
from _thread import *

hostname = socket.gethostname()
HOST = socket.gethostbyname(hostname) 
PORT = 65432      

BUFF_SIZE = 1024
N = 5                   # số client tối đa kết nối đồng thời đến server
threadCount = 0

ADMIN_USR = "admin"     
ADMIN_PSW = "adm"

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
def login(sock):
    usr = ""
    psw = ""
    usr = receive(sock)
    psw = receive(sock)
            
    fd = open("account.json", "r")
    userExist = False
    accs = json.loads(fd.read())
    for acc in accs["account"]:
        u = acc["usr"]
        p = acc["psw"]
        if u == usr:
            if p == psw:
                sendData(sock, '1') # Đăng nhập thành công
            else:
                sendData(sock, '-1') # Sai mật khẩu
            userExist = True
    if not userExist:
        sendData(sock, '0') # Tài khoản không tồn tại
    fd.close()

# Đăng ký
def regist(sock):
    usr = ""
    psw = ""
    usr = receive(sock)
    psw = receive(sock)

    fd = open("account.json", "r+")
    userExist = False
    accs = json.loads(fd.read())
    for acc in accs["account"]:
        u = acc["usr"]
        if u == usr:
            sendData(sock, '0') # Tên đăng nhập đã tồn tại
            userExist = True
            return False
    if not userExist:
        accs["account"].append({"usr": usr,"psw": psw})
        accs.update(accs)
        fd.seek(0)
        json.dump(accs, fd, indent = 4)
        sendData(sock, '1') # Đăng ký thành công
    fd.close()
    return True

def matchDetail(sock):
    id = receive(sock)
    f = open("matchDetail.json", "r")
    data = json.load(f)
    f.close()
    
    f1 = open("listscore.json", "r")
    general = json.load(f1)
    f1.close()

    pos1 = -1
    pos2 = -1

    for i in range(0,len(general["list"])):
        if (general["list"][i]["id"] == id):
            pos1 = i

    for i in range(0,len(data["match"])):
        if (data["match"][i]["id"] == id):
            pos2 = i

    if (pos1 != -1 and pos2 != -1):
        res = general["list"][pos1]
        res["events"] = data["match"][pos2]["events"]
        sendData(sock, json.dumps(res))

    sendData(sock, '0')
    return False

### ADMIN ###

# Đăng nhập
def adminLog(sock):
    usr = receive(sock)
    psw = receive(sock)
    if (usr == ADMIN_USR and psw == ADMIN_PSW):
        sendData(sock, '1') # Admin đăng nhập thành công
        return True
    else:
        sendData(sock, '-1') # Admin đăng nhập không thành công
        return False

# Thêm trận
def addMatch(sock):
    data_add = receive(sock)
    data_add = json.loads(data_add)
    f = open("listscore.json", "r+")
    data = json.load(f)

    for match in data["list"]:
        if (match["id"] == data_add["id"]):     # ID trận đã tồn tại
            sendData(sock, '0')     # Thêm trận đấu không thành công
            f.close()
            return False
    
    data["list"].append(data_add)
    f.seek(0)
    json.dump(data, f, indent = 4)
    sendData(sock, '1')     # Thêm trận đấu thành công
    f.close()
    return True

# Cập nhật trận đấu (score, time)
def updMatch(sock):   
    data_add = receive(sock)  
    data_add = json.loads(data_add)    
    f = open("listscore.json", "r+")
    data = json.load(f)
    matches = data["list"]
    pos = -1

    for i in range (0,len(matches)):
        if (matches[i]["id"] == data_add["id"]):
            pos = i

    if (pos != -1):
        data["list"][pos]["time"] = data_add["time"]
        data["list"][pos]["score"] = data_add["score"]
        f.seek(0)
        json.dump(data, f, indent = 4)
        sendData(sock, '1')     # Cập nhật thành công
        f.close()
        return True
    
    sendData(sock, '0')     # Cập nhật thất bại
    f.close()
    return False

# Cập nhật sự kiện
def updEvent(sock):
    data_add = receive(sock)  
    data_add = json.loads(data_add)    
    f = open("matchDetail.json", "r+")
    data = json.load(f)
    matches = data["match"]
    pos = -1

    for i in range (0,len(matches)):
        if (matches[i]["id"] == data_add["matchID"]):
            pos = i

    if (pos != -1):
        data["match"][pos]["events"][data_add["eventID"]] = data_add["event"]
        data.update(data)
        f.seek(0)
        json.dump(data, f, indent = 4)
        sendData(sock, '1')     # Cập nhật thành công
        f.close()
        return True
    
    sendData(sock, '0')     # Cập nhật thất bại
    f.close()
    return False

# Thêm event
def addEvent(sock):   
    data_add = receive(sock)  
    data_add = json.loads(data_add)    # Mỗi lần thêm 1 event trong 1 trận
    f = open("matchDetail.json", "r+")
    data = json.load(f)
    matches = data["match"]
    pos = -1

    for i in range (0,len(matches)):
        if (matches[i]["id"] == data_add["id"]):
            pos = i

    if (pos != -1):
        data["match"][pos]["events"].append(data_add["events"][0])
        data.update(data)
        f.seek(0)
        json.dump(data, f, indent = 4)
        sendData(sock, '1')     # Thêm sự kiện thành công
        f.close()
        return True
    
    sendData(sock, '0')     # Thêm sự kiện thất bại
    f.close()
    return False

###############


def threadClient(conn):
    str = ""
    checkAd = False
    while True:
        str = receive(conn)
        print(str)

        ### ADMIN ###
        if (str == "ADLOG"):
            str = receive(conn)
            if (str == "LOG"):
                checkAd = adminLog(conn)

            while checkAd:
                str = receive(conn)
                if (str == "ADDEV"):
                    str = receive(conn)
                    if (str == "ADD"):
                        addEvent(conn)

                elif (str == "ADDMT"):
                    str = receive(conn)
                    if (str == "ADD"):
                        addMatch(conn)

                elif (str == "UPDMT"):
                    str = receive(conn)
                    if (str == "UPD"):
                        updMatch(conn)

                elif (str == "UPDEV"):
                    str = receive(conn)
                    if (str == "UPD"):
                        updEvent(conn)

                else:   # QUIT
                    checkAd = False
                    break

        ###########

        elif (str == "LOGIN"):
            str = receive(conn)
            if (str == "LOG"):
                login(conn)

        elif (str == "REGIST"):
            while True:
                str = receive(conn)
                if (str == "REG"):
                    flag = regist(conn)
                    if flag:
                        break
                else:
                    break
            
        elif (str == "DETAIL"):
            str = receive(conn)
            while True:
                if (str == "DET"):
                    matchDetail(conn)
                else:
                    break

        else:
            break
    conn.close()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(N)

sock_clients = []
#start_new_thread(closingServer, ())

try:
    while True:
        client, addr = s.accept()
        sock_clients.append(client)
        print('Connected by', addr)
        start_new_thread(threadClient, (client, ))
        threadCount += 1
        print("Thread num: ", threadCount)
        
except KeyboardInterrupt:
    s.close()