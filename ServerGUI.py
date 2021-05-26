from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from functools import partial
import socket
#from socket import AF_INET, socket, SOCK_STREAM
import json

hostname = socket.gethostname()
HOST = socket.gethostbyname(hostname) 
PORT = 65432 
print(HOST)

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

class serverGUI(object):
    def __init__(self,master):
        self.master = master
        self.master.title("Open Server")
        frame1 = Frame(master= self.master, width=150, height=150)
        frame1.pack()
        button = Button(master = self.master, text="Mở server", width=10, height=5, command=self.open)
        button.place(x=35, y=30)
        self.master.mainloop()

    def openGUI(self):
        self.master.withdraw()
        self.master1 = Toplevel(self.master)
        self.master1.title("Server") 
        self.master1.geometry("500x350") 
        self.master1.resizable(0, 0)
        Label(self.master1, text = "LIVE SCORE", fg = 'blue',font = ('Times', 30, 'bold')).pack(side = TOP, pady = 2)
        Label(self.master1, text = "SERVER", fg = 'blue',font = ('Times', 20)).pack(side = TOP, pady = 5)
        self.T = Text(self.master1, height = 15, width = 55)
        self.T.pack()
        self.master1.mainloop()

    def open(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            self.master.withdraw()
            self.master1 = Toplevel(self.master)
            self.master1.title("Server") 
            self.master1.geometry("500x350") 
            self.master1.resizable(0, 0)
            Label(self.master1, text = "LIVE SCORE", fg = 'blue',font = ('Times', 30, 'bold')).pack(side = TOP, pady = 2)
            Label(self.master1, text = "SERVER", fg = 'blue',font = ('Times', 20)).pack(side = TOP, pady = 5)
            self.T = Text(self.master1, height = 15, width = 55)
            self.T.pack()
            self.master1.mainloop()
            with conn:
                self.T.insert(END, "Connected by: " + addr + "\n") 
                str = ""
                while True:
                    str = receive(conn)
                    print(str)
                    self.T.insert(END, str + "-")
                    if (str == "LOGIN"):
                        while True:
                            str = receive(self.sock)
                            if (str == "LOG"):
                                self.login()
                            elif (str == "REGIST"):
                                while True:
                                    str = receive(self.sock)
                                    if (str == "REG"):
                                        flag = self.regist()
                                        if flag:
                                            break
                                    else:
                                        break
                            else:
                                continue                           
                    else: 
                        break
            self.sock.close()
            self.T.insert(END, "QUIT") 
        
    # Đăng nhập
    def login(self):
        usr = ""
        psw = ""
        usr = receive(self.sock)
        self.T.insert(END, "usr: " + usr + "-")
        psw = receive(self.sock)
        self.T.insert(END, "psw: " + psw + "-")    
        fd = open("account.json", "r")
        userExist = False
        accs = json.loads(fd.read())
        for acc in accs["account"]:
            u = acc["usr"]
            p = acc["psw"]
            if u == usr:
                if p == psw:
                    sendData(self.sock, '1') # Đăng nhập thành công
                    self.T.insert(END, "Đăng nhập thành công \n")
                else:
                    sendData(self.sock, '-1') # Sai mật khẩu
                    self.T.insert(END, "Sai mật khẩu \n")
                userExist = True
        if not userExist:
            sendData(self.sock, '0') # Tài khoản không tồn tại
            self.T.insert(END, "Tài khoản không tồn tại \n")
        fd.close()

    # Đăng ký
    def regist(self):
        usr = ""
        psw = ""
        usr = receive(self.sock)
        self.T.insert(END, "usr: " + usr + "-")
        psw = receive(self.sock)
        self.T.insert(END, "psw: " + psw + "-") 
        fd = open("account.json", "r+")
        userExist = False
        accs = json.loads(fd.read())
        for acc in accs["account"]:
            u = acc["usr"]
            if u == usr:
                sendData(self.sock, '0') # Tên đăng nhập đã tồn tại
                userExist = True
                self.T.insert(END, "Tên đăng nhập đã tồn tại \n")
                return False
        if not userExist:
            accs["account"].append({"usr": usr,"psw": psw})
            accs.update(accs)
            fd.seek(0)
            json.dump(accs, fd, indent = 4)
            sendData(self.sock, '1') # Đăng ký thành công
            self.T.insert(END, "Đăng ký thành công \n")
        fd.close()
        return True

#Main
if __name__ == "__main__":
    root = Tk()
    window = serverGUI(root)
    root.mainloop()

