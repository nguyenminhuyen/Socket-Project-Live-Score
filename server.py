from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from functools import partial
from _thread import *
import socket
#from socket import AF_INET, socket, SOCK_STREAM
import json

hostname = socket.gethostname()
HOST = socket.gethostbyname(hostname) 
PORT = 65432 

BUFF_SIZE = 1024
N = 5                   # số client tối đa kết nối đồng thời đến server

ADMIN_USR = "admin"     
ADMIN_PSW = "adm"

#Create socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    messagebox.showerror("Error", "Lỗi không thể tạo socket")

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

class runServerGUI(object):
    def __init__(self,master):
        self.master = master
        self.sock = None
        self.threadCount = 0
        self.master.title("Server")
        self.master.geometry("500x400")
        self.master.resizable(0, 0)
        Label(self.master, text = "LIVE SCORE", fg = 'blue',font = ('Times', 30, 'bold')).pack(side = TOP, pady = 2)
        Label(self.master, text = "Server", fg = 'blue',font = ('Times', 20)).pack(side = TOP, pady = 5) 
        createFunc = partial(self.create, self.master)
        Button(master = self.master, text="Open server", width= 15, height=2, command= createFunc).pack (side = TOP, pady = 5)
        self.scroll_bar = Scrollbar(self.master, orient=VERTICAL)
        self.T = Text(self.master,font = ('Times',12), height = 12, width = 55, yscrollcommand= self.scroll_bar.set)
        self.scroll_bar.pack( side = LEFT, padx = 1)
        self.scroll_bar.config(command=self.T.yview)
        self.T.pack()
        self.master.mainloop()

    def run(self, msg):
        self.T.configure(state="normal")
        self.T.insert(END,msg)
        self.T.configure(state="disabled")
        return

    def create(self, master):
        self.master1 = Toplevel(master)
        self.master1.title("Server")
        self.master1.geometry("400x200") 
        self.master1.resizable(0, 0)
        Label(self.master1, text = "LIVE SCORE", fg = 'blue',font = ('Times', 30, 'bold')).pack(side = TOP, pady = 2)
        Label(self.master1, text = "Client", fg = 'blue',font = ('Times', 20)).pack(side = TOP, pady = 5)
        Label(self.master1, text = "Nhập số client cho phép kết nối: ").pack(side = TOP, pady = 5)
        nVar = StringVar()
        nEntry = Entry(self.master1,textvariable= nVar, width = 50).pack(side = TOP, pady = 2)
        submittedHost = nVar.get()
        nFunc = partial(self.createThread,nVar)
        Button(self.master1, text = "Submit", command = nFunc).pack(side = TOP, pady = 2)
        self.master1.mainloop()

    def createThread(self, nVar):
        #self.master1.withdraw()
        s.bind((HOST, PORT))
        s.listen(int(nVar.get()))
        try:
            while True:
                self.sock, addr = s.accept()
                print('Connected by', addr)
                msg = " Connected by: " + str(addr) + "\n"
                self.run(msg)
                start_new_thread(self.threadClient,())
                self.threadCount += 1
                print("Thread num: ", self.threadCount)
                msg = "Thread num: " + str(self.threadCount) + "\n"
                self.run(msg)
        except KeyboardInterrupt:
            s.close()

    def threadClient(self):
        str = ""
        checkAd = False
        while True:
            str = receive(self.sock)
            print(str)
            self.run(str)
            ### ADMIN ###
            if (str == "LOGIN"):
                str = receive(self.sock)
                print(str)
                self.run(str)
                while True:
                    if (str == "LOG"):
                        checkAd = self.login()
                        if (checkAd):
                            while True:
                                str = receive(self.sock)
                                print(str)
                                self.run(str)
                                if (str == "ADDEV"):
                                    str = receive(self.sock)
                                    if (str == "ADD"):
                                        self.addEvent()

                                elif (str == "ADDMT"):
                                    str = receive(self.sock)
                                    if (str == "ADD"):
                                        self.addMatch()

                                elif (str == "UPDSC"):
                                    str = receive(self.sock)
                                    if (str == "UPD"):
                                        self.updMatch(0)

                                elif (str == "UPDTM"):
                                    str = receive(self.sock)
                                    if (str == "UPD"):
                                        self.updMatch(1)

                                elif (str == "UPDEV"):
                                    str = receive(self.sock)
                                    if (str == "UPD"):
                                        self.updEvent()

                                else:   # QUIT
                                    break

                        else:
                            str = receive(self.sock)
                            print(str)
                            self.run(str)
                            if (str == "LIST"):
                                self.listScore()
                                while True:
                                    str = receive(self.sock)
                                    print(str)
                                    self.run(str)
                                    if (str == "DETAIL"):
                                        str = receive(self.sock)
                                        while True:
                                            if (str == "DET"):
                                                self.matchDetail()
                                            else:
                                                break
                                    else:
                                        break
                    
                    elif (str == "REGIST"):
                        while True:
                            str = receive(self.sock)
                            print(str)
                            self.run(str)
                            if (str == "REG"):
                                flag = self.regist(self.sock)
                                if flag:
                                    break
                            else:
                                break
                    else:
                        break
            else:
                break
        self.sock.close()

    # Đăng nhập
    def login(self):
        usr = ""
        psw = ""
        usr = receive(self.sock)
        psw = receive(self.sock)
        if (usr == ADMIN_USR and psw == ADMIN_PSW):
            sendData(self.sock, '2') # Admin đăng nhập thành công
            return True     
        fd = open("account.json", "r")
        userExist = False
        accs = json.loads(fd.read())
        for acc in accs["account"]:
            u = acc["usr"]
            p = acc["psw"]
            if u == usr:
                if p == psw:
                    sendData(self.sock, '1') # Đăng nhập thành công
                else:
                    sendData(self.sock, '-1') # Sai mật khẩu
                userExist = True
        if not userExist:
            sendData(self.sock, '0') # Tài khoản không tồn tại
        fd.close()
        return False

    # Đăng ký
    def regist(self):
        usr = ""
        psw = ""
        usr = receive(self.sock)
        psw = receive(self.sock)

        fd = open("account.json", "r+")
        userExist = False
        accs = json.loads(fd.read())
        for acc in accs["account"]:
            u = acc["usr"]
            if u == usr:
                sendData(self.sock, '0') # Tên đăng nhập đã tồn tại
                userExist = True
                return False
        if not userExist:
            accs["account"].append({"usr": usr,"psw": psw})
            accs.update(accs)
            fd.seek(0)
            json.dump(accs, fd, indent = 4)
            sendData(self.sock, '1') # Đăng ký thành công
        fd.close()
        return True

    def matchDetail(self):
        id = receive(self.sock)
        f = open("matchDetail.json", "r")
        data = json.load(f)
        f.close()

        for mch in data["match"]:
            if mch["id"] == id:
                sendData(self.sock, json.dumps(mch["events"]))
                return True

        sendData(self.sock, '0')
        return False

    def listScore(self):
        f = open("listScore.json", "r")
        data = json.load(f)
        f.close()

        for scr in data["score"]:
            sendData(self.sock, json.dumps(scr))

        return True

    # Thêm trận
    def addMatch(self):
        data_add = receive(self.sock)
        data_add = json.loads(data_add)
        f = open("listscore.json", "r+")
        data = json.load(f)

        for match in data["list"]:
            if (match["id"] == data_add["id"]):     # ID trận đã tồn tại
                sendData(self.sock, '0')     # Thêm trận đấu không thành công
                f.close()
                return False
        
        data["list"].append(data_add)
        f.seek(0)
        json.dump(data, f, indent = 4)
        sendData(self.sock, '1')     # Thêm trận đấu thành công
        f.close()
        return True

    # Cập nhật tỉ số
    def updMatch(self, mode):   # mode 0: update score, mode 1: update time
        data_add = receive(self.sock)  
        data_add = json.loads(data_add)    
        f = open("listscore.json", "r+")
        data = json.load(f)
        matches = data["list"]
        pos = -1
        upd = ""
        if (mode == 0):
            upd = "score"
        else:
            upd = "time"

        for i in range (0,len(matches)):
            if (matches[i]["id"] == data_add["id"]):
                pos = i

        if (pos != -1):
            data["list"][pos][upd] = data_add[upd]
            f.seek(0)
            json.dump(data, f, indent = 4)
            sendData(self.sock, '1')     # Cập nhật thành công
            f.close()
            return True
        
        sendData(self.sock, '0')     # Cập nhật thất bại
        f.close()
        return False

    # Cập nhật sự kiện
    def updEvent(self):
        data_add = receive(self.sock)  
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
            sendData(self.sock, '1')     # Cập nhật thành công
            f.close()
            return True
        
        sendData(self.sock, '0')     # Cập nhật thất bại
        f.close()
        return False

    # Thêm event
    def addEvent(self):   
        data_add = receive(self.sock)  
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
            sendData(self.sock, '1')     # Thêm sự kiện thành công
            f.close()
            return True
        
        sendData(self.sock, '0')     # Thêm sự kiện thất bại
        f.close()
        return False

###############

#Main
if __name__ == "__main__":
    root = Tk()
    window = runServerGUI(root)
    root.mainloop()