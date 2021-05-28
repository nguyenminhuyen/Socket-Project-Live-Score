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
    # usr = ""
    # psw = ""
    # usr = receive(sock)
    # print(usr + "\n")
    # psw = receive(sock)
    # print(psw)
    sub = receive(sock)
    sub = json.loads(sub)
    if (sub['usr'] == ADMIN_USR and sub['psw'] == ADMIN_PSW):
        print(2)
        sendData(sock, '2') # Admin đăng nhập thành công
        return 2        
    fd = open("account.json", "r")
    userExist = False
    accs = json.loads(fd.read())
    for acc in accs["account"]:
        u = acc["usr"]
        p = acc["psw"]
        if u == sub['usr']:
            if p == sub['psw']:
                sendData(sock, '1') # Đăng nhập thành công
                print(1)
                return 1
            else:
                sendData(sock, '-1') # Sai mật khẩu
                print(-1)
                return -1
            userExist = True
    if not userExist:
        sendData(sock, '0') # Tài khoản không tồn tại
        print(0)
        return 0
    fd.close()

# Đăng ký
def regist(sock):
    # usr = ""
    # psw = ""
    # usr = receive(sock)
    # psw = receive(sock)
    sub = receive(sock)
    sub = json.loads(sub)
    fd = open("account.json", "r+")
    userExist = False
    accs = json.loads(fd.read())
    for acc in accs["account"]:
        u = acc["usr"]
        if u == sub['usr']:
            sendData(sock, '0') # Tên đăng nhập đã tồn tại
            userExist = True
            return False
    if not userExist:
        accs["account"].append(sub)
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
    
    f1 = open("listmatch.json", "r")
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
        for evn in data["match"][pos2]["events"]:
            str = {'id': id, 'time': evn['time'], 'type' : evn['type'], 'team': evn['team'], 'player': evn['player'], 'assist': evn['assist'], 'score': evn['score']}
            sendData(sock, json.dumps(str))
            print(str)

    sendData(sock, '0')
    return False

def listMatch(sock):
    f = open("listmatch.json", "r")
    data = json.load(f)
    f.close()
    #sendData(sock, json.dumps(data["list"]))
    #print(data["list"])
    for sc in data["list"]:
        sendData(sock, json.dumps(sc))
        print(sc)
    sendData(sock, '0')
    return False
    
### ADMIN ###

# Thêm trận
def addMatch(sock):
    data_add = receive(sock)
    data_add = json.loads(data_add)
    f = open("listmatch.json", "r+")
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
    f = open("listmatch.json", "r+")
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

# Thêm event
def upEvent(sock):   
    data_add = receive(sock)  
    data_add = json.loads(data_add)    # Mỗi lần thêm 1 event trong 1 trận
    print (data_add)
    f = open("matchDetail.json", "r+")
    data = json.load(f)
    matches = data["match"]
    pos = -1

    for i in range (0,len(matches)):
        if (matches[i]["id"] == data_add["id"]):
            pos = i
    print(pos)
    if (pos != -1):
        data["match"][pos]["events"].append(data_add["events"])
        data.update(data)
        f.seek(0)
        json.dump(data, f, indent = 4)
        sendData(sock, '1')     # Thêm sự kiện thành công
        print(1)
        f.close()
        return True
    
    sendData(sock, '0')     # Thêm sự kiện thất bại
    print(0)
    f.close()
    return False

###############


def threadClient(conn):
    str = ""
    checkAd = False
    while True:
        str = receive(conn)
        print(str)
        if (str == "LOGIN"):
            signal = login(conn)
            if (signal == 2):
                while True:
                    str = receive(conn)
                    print(str)
                    if (str == "ADDMT"):
                        addMatch(conn)
                    elif (str == "UPDMT"):
                        updMatch(conn)
                    elif (str == "UPDEV"):
                        upEvent(conn)
                    else:
                        break
            elif (signal == 1):
                while True:
                    str = receive(conn)
                    print(str)
                    if (str == "LISTMT"):
                        listMatch(conn)
                    elif (str == "MTCDT"):
                        matchDetail(conn)
                    else:
                        break
        elif (str == "REGIST"):
            flag = regist(conn)
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