import socket
import json
from _thread import *
import logging
from serverGUI import*

hostname = socket.gethostname()
HOST = socket.gethostbyname(hostname) 
PORT = 65432      

BUFF_SIZE = 1024
NClient = 5                   # số client tối đa kết nối đồng thời đến server
threadCount = 0

ADMIN_USR = "admin"     
ADMIN_PSW = "adm"


class Server:
    def __init__(self, logger,mClient = NClient, host = HOST, port = PORT, ):
        self.host = host
        self.port = port
        self.NClient = mClient
        self.logger = logger
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.threadCount = 0
        self.sock_clients = []
        self.connect()
        #start_new_thread(closingServer, ())

    def connect(self):
        self.logger.log(logging.INFO,"Cho phép tối đa" + str(self.NClient) + "được kết nối.")
        self.s.bind((HOST, PORT))
        self.s.listen(self.NClient)
        try:
            while True:
                client, addr = self.s.accept()
                self.sock_clients.append(client)
                self.logger.log(logging.RESULT,"Connected by " + str(addr))
                print('Connected by', addr)
                start_new_thread(self.threadClient, (client, ))
                self.threadCount += 1
                self.logger.log(logging.RESULT,"Thread num: " + self.threadCount)
                print("Thread num: ", self.threadCount)
        except KeyboardInterrupt:
            self.s.close()

    ###############
    def sendData(self,sock, msg):
        sock.sendall(bytes(msg, "utf8"))

    def receive(self, sock): 
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
    def login(self,sock):
        # usr = ""
        # psw = ""
        # usr = receive(sock)
        # print(usr + "\n")
        # psw = receive(sock)
        # print(psw)
        sub = self.receive(sock)
        sub = json.loads(sub)
        self.logger.log(logging.DATA,"Usr:" + str(sub['usr']) + " - Pass:" + str(sub['psw']))   
        if (sub['usr'] == ADMIN_USR and sub['psw'] == ADMIN_PSW):
            print(2)
            self.sendData(sock, '2') # Admin đăng nhập thành công
            self.logger.log(logging.RESULT,"Đăng nhập admin thành công")
            return 2    
        fd = open("account.json", "r")
        userExist = False
        accs = json.loads(fd.read())
        for acc in accs["account"]:
            u = acc["usr"]
            p = acc["psw"]
            if u == sub['usr']:
                if p == sub['psw']:
                    self.sendData(sock, '1') # Đăng nhập thành công
                    self.logger.log(logging.RESULT,"Đăng nhập thành công")
                    return 1
                else:
                    self.sendData(sock, '-1') # Sai mật khẩu
                    self.logger.log(logging.ERROR,"Sai mật khẩu")
                    print(-1)
                    return -1
                userExist = True
        if not userExist:
            self.sendData(sock, '0') # Tài khoản không tồn tại
            self.logger.log(logging.ERROR,"Tài khoản không tồn tại")
            print(0)
            return 0
        fd.close()

    # Đăng ký
    def regist(self, sock):
        # usr = ""
        # psw = ""
        # usr = receive(sock)
        # psw = receive(sock)
        sub = self.receive(sock)
        sub = json.loads(sub)
        self.logger.log(logging.DATA,"Usr:" + sub['usr'] + " - Pass:" + sub['psw']) 
        fd = open("account.json", "r+")
        userExist = False
        accs = json.loads(fd.read())
        for acc in accs["account"]:
            u = acc["usr"]
            if u == sub['usr']:
                self.sendData(sock, '0') # Tên đăng nhập đã tồn tại
                self.logger.log(logging.ERROR,"Tên đăng nhập đã tồn tại")
                userExist = True
                return False
        if not userExist:
            accs["account"].append(sub)
            accs.update(accs)
            fd.seek(0)
            json.dump(accs, fd, indent = 4)
            self.sendData(sock, '1') # Đăng ký thành công
            self.logger.log(logging.RESULT,"Đăng ký thành công")
        fd.close()
        return True

    def matchDetail(self,sock):
        id = self.receive(sock)
        self.logger.log(logging.DATA,"ID trận đấu cần mở: " + id)
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
            res = general["list"][pos1]
            res["events"] = data["match"][pos2]["events"]
            self.sendData(sock, json.dumps(res))
            self.logger.log(logging.RESULT,"Mở match detail thành công")
        else:
            self.sendData(sock, '-1') #Khong ton tai match detail
            self.logger.log(logging.ERROR,"Không tồn tại match detail")
        self.sendData(sock, '0')
        return False

    #List Match
    def listMatch(self,sock):
        f = open("listmatch.json", "r")
        data = json.load(f)
        f.close()
        self.sendData(sock, json.dumps(data))
        self.logger.log(logging.RESULT,"Mở danh sách trận đấu thành công")
        #self.sendData(sock, '0')
        return False
        
    ### ADMIN ###

    # Thêm trận
    def addMatch(self,sock):
        data_add = self.receive(sock)
        data_add = json.loads(data_add)
        self.logger.log(logging.DATA,str(data_add))
        f = open("listmatch.json", "r+")
        data = json.load(f)

        for match in data["list"]:
            if (match["id"] == data_add["id"]):     # ID trận đã tồn tại
                self.sendData(sock, '0')     # Thêm trận đấu không thành công
                self.logger.log(logging.ERROR,"ID trận đã tồn tại - Thêm trận đấu không thành công")
                f.close()
                return False
        
        data["list"].append(data_add)
        f.seek(0)
        json.dump(data, f, indent = 4)
        self.sendData(sock, '1')     # Thêm trận đấu thành công
        self.logger.log(logging.RESULT,"Thêm trận đấu thành công")
        f.close()
        return True

    # Cập nhật trận đấu (score, time)
    def updMatch(self, sock):   
        data_add = self.receive(sock)  
        data_add = json.loads(data_add) 
        self.logger.log(logging.DATA,str(data_add))   
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
            self.sendData(sock, '1')     # Cập nhật thành công
            self.logger.log(logging.RESULT,"Cập nhật trận đấu (score, time) thành công")
            f.close()
            return True
        
        self.sendData(sock, '0')     # Cập nhật thất bại
        self.logger.log(logging.ERROR,"Cập nhật trận đấu (score, time) thất bại")
        f.close()
        return False

    # Thêm event
    def upEvent(self, sock):   
        data_add = self.receive(sock)  
        data_add = json.loads(data_add)    # Mỗi lần thêm 1 event trong 1 trận
        self.logger.log(logging.DATA,str(data_add))
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
            self.sendData(sock, '1')     # Thêm sự kiện thành công
            self.logger.log(logging.RESULT,"Thêm sự kiện thành công")
            print(1)
            f.close()
            return True
        
        self.sendData(sock, '0')     # Thêm sự kiện thất bại
        self.logger.log(logging.ERROR,"Thêm sự kiện thất bại")
        print(0)
        f.close()
        return False

    def threadClient(self, conn):
        str = ""
        checkAd = False
        while True:
            str = self.receive(conn)
            print(str)
            self.logger.log(logging.INFO,str)
            if (str == "LOGIN"):
                signal = self.login(conn)
                if (signal == 2):
                    while True:
                        str = self.receive(conn)
                        print(str)
                        if (str == "ADDMT"):
                            self.addMatch(conn)
                        elif (str == "UPDMT"):
                            self.updMatch(conn)
                        elif (str == "UPDEV"):
                            self.upEvent(conn)
                        else:
                            break
                elif (signal == 1):
                    while True:
                        str = self.receive(conn)
                        print(str)
                        if (str == "LISTMT"):
                            self.listMatch(conn)
                        elif (str == "MTCDT"):
                            self.matchDetail(conn)
                        else:
                            break
            elif (str == "REGIST"):
                flag = self.regist(conn)
            else:
                break
        conn.close()
