from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from functools import partial
from socket import AF_INET, socket, SOCK_STREAM
BUFF_SIZE = 1024

#Create socket
try:
    sclient = socket(AF_INET, SOCK_STREAM)
except socket.error:
    messagebox.showerror("Error", "Lỗi không thể tạo socket")

def sendData(sclient, msg):
    sclient.sendall(bytes(msg, "utf8"))

def receive(sclient): 
    data = b''
    while True:
        while True:
            part = sclient.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                break
        if data:
            break
    return data.decode().strip()

class matchDetailGUI(object):
    def __init__(self, master):
        self.master1 = Toplevel(master)
        self.master1.title("DANH SÁCH TRẬN ĐẤU") 
        self.master1.geometry("700x350") 
        self.master1.resizable(0, 0)
        Label(self.master1, text = "LIVE SCORE", fg = 'blue',font = ('Times', 30, 'bold')).pack(side = TOP, pady = 2)
        Label(self.master1, text = "MATCH DETAIL", fg = 'blue',font = ('Times', 20)).pack(side = TOP, pady = 5)
        self.treev = ttk.Treeview(self.master1, selectmode ='browse')
        self.treev.pack(side =TOP)
        verscrlbar = ttk.Scrollbar(self.master1, orient ="vertical", command = self.treev.yview)
        verscrlbar.pack(side ='right', fill ='x')
        self.treev.configure(xscrollcommand = verscrlbar.set)
        self.treev["columns"] = ("1", "2", "3", "4", "5")
        self.treev['show'] = 'headings'
        self.treev.column("1", width = 110, anchor ='c')
        self.treev.column("2", width = 120, anchor ='se')
        self.treev.column("3", width = 160, anchor ='se')
        self.treev.column("4", width = 120, anchor ='se')
        self.treev.column("5", width = 160, anchor ='se')
        self.treev.heading("1", text ="ID Score")
        self.treev.heading("2", text ="Time")
        self.treev.heading("3", text ="Team 1")
        self.treev.heading("4", text = "Score")
        self.treev.heading("5", text = "Team 2")
        self.master1.mainloop()

class xemDSGUI(object):
    def __init__(self, master):
        self.master1 = master
        self.master1.title("DANH SÁCH TRẬN ĐẤU") 
        self.master1.geometry("700x400") 
        self.master1.resizable(0, 0)
        Label(self.master1, text = "LIVE SCORE", fg = 'blue',font = ('Times', 30, 'bold')).pack(side = TOP, pady = 2)
        Label(self.master1, text = "LIST SCORE", fg = 'blue',font = ('Times', 20)).pack(side = TOP, pady = 5)
        Button(self.master1, text = "Hiển thị danh sách trận đấu", command = self.master1.destroy).pack(side = TOP, pady = 5)
        self.topFrame = Frame(self.master1)
        self.topFrame.pack(side = TOP, pady = 2, padx = 5)
        Label(self.topFrame, text = "Match detail", font = ('Time', 11, 'bold')).pack(side = LEFT, padx = 2)
        IDVar = StringVar()
        IDVar.set("Nhập ID")
        hostEntry = Entry(self.topFrame,textvariable=IDVar, width = 50).pack(side = LEFT, padx = 2)
        submittedHost = IDVar.get()
        #connectFunc = partial(self.connectServer,IDVar)
        Button(self.topFrame, text = "Xem", command = self.master1.destroy).pack(side = LEFT)
        self.bottomFrame = Frame(self.master1)
        self.bottomFrame.pack(side = TOP, fill = X )
        self.treev = ttk.Treeview(self.bottomFrame, selectmode ='browse')
        self.treev.pack(side =TOP)
        verscrlbar = ttk.Scrollbar(self.bottomFrame, orient ="vertical", command = self.treev.yview)
        verscrlbar.pack(side ='right', fill ='x')
        self.treev.configure(xscrollcommand = verscrlbar.set)
        self.treev["columns"] = ("1", "2", "3", "4", "5")
        self.treev['show'] = 'headings'
        self.treev.column("1", width = 110, anchor ='c')
        self.treev.column("2", width = 120, anchor ='se')
        self.treev.column("3", width = 160, anchor ='se')
        self.treev.column("4", width = 120, anchor ='se')
        self.treev.column("5", width = 160, anchor ='se')
        self.treev.heading("1", text ="ID Score")
        self.treev.heading("2", text ="Time")
        self.treev.heading("3", text ="Team 1")
        self.treev.heading("4", text = "Score")
        self.treev.heading("5", text = "Team 2")
        self.master1.mainloop()
  

class adminGUI(object):
    def __init__(self,master):
        self.master = master
        self.master.title("Client admin") 
        self.master.geometry("500x350") 
        self.master.resizable(0, 0)
        Label(self.master, text = "LIVE SCORE", fg = 'blue',font = ('Times', 30, 'bold')).pack(side = TOP, pady = 2)
        Label(self.master, text = "ADMIN", fg = 'blue',font = ('Times', 20)).pack(side = TOP, pady = 7)
        Button(self.master, text = "Thêm trận", height = 2, width = 30, command = self.master.destroy,).pack(side = TOP, pady = 2)
        Button(self.master, text = "Cập nhật tỉ số", height = 2, width = 30, command = self.master.destroy).pack(side = TOP, pady = 2)
        Button(self.master, text = "Cập nhật sự kiện", height = 2, width = 30, command = self.master.destroy).pack(side = TOP, pady = 2)
        Button(self.master, text = "Thêm event", height = 2, width = 30, command = self.master.destroy).pack(side = TOP, pady = 2)
        self.master.mainloop()

class logInGUI(object):

    #Log In GUI
    def __init__(self, master):
        master.withdraw()
        self.master = Toplevel(master)
        self.sclient = sclient
        sendData(self.sclient, "LOGIN")
        self.master.title("Client") 
        self.master.geometry("500x350") 
        self.master.resizable(0, 0)
        Label(self.master, text = "LIVE SCORE", fg = 'blue',font = ('Times', 30, 'bold')).pack(side = TOP, pady = 2)
        Label(self.master, text = "LOG IN", fg = 'blue',font = ('Times', 20)).pack(side = TOP, pady = 5)
        userLabel = Label(self.master, text = "User Name: ", font = ('Times', 12, 'bold'))
        userLabel.pack(side = TOP, pady = 2)
        userVar = StringVar()
        userEntry = Entry(self.master,textvariable= userVar, width = 50)
        userEntry.pack(side = TOP, pady = 2)
        passVar = StringVar()
        passLabel = Label(self.master, text = "Password: ",font = ('Times', 12, 'bold'))
        passLabel.pack(side = TOP, pady = 2)
        passEntry = Entry(self.master,textvariable= passVar,show = "*", width = 50)
        passEntry.pack(side = TOP, pady = 5)
        logInFunc = partial(self.logIn, userVar, passVar)
        logInButton = Button(self.master, text = "LOG IN", width = 10, height = 1,font = ('Times', 12, 'bold'), command = logInFunc)
        logInButton.pack(side = TOP, pady = 5)
        signInLabel = Label(self.master, text = "Nếu bạn chưa có tài khoản", font = ('Times', 12, 'italic')).pack(side = TOP, pady = 5)
        signInButton = Button(self.master, text = "SIGN IN", width = 10, height = 1, font = ('Times', 12, 'bold'), command = self.signInGUI)
        signInButton.pack(side = TOP)
        #self.master.protocol("WM_DELETE_WINDOW", self.Closing)
        self.master.mainloop()

    #Log In Func
    def logIn(self, userVar, passVar):
        print("LOG")
        submittedUser = userVar.get()
        print(submittedUser + "\n")
        sendData(self.sclient, "LOG")
        sendData(self.sclient, submittedUser)
        submittedPass = passVar.get()
        print(submittedPass)
        sendData(self.sclient, submittedPass)
        signal = receive(self.sclient)
        if (signal == '2'):
            messagebox.showinfo("Info", "Đăng nhập admin thành công")
            return True
        elif (signal == '1'):
           messagebox.showinfo("Info", "Đăng nhập thành công")
           return True
        elif (signal == '-1'):
           messagebox.showwarning("Warning", "Sai mật khẩu")
           return False
        else:
           messagebox.showwarning("Warning", "Tài khoản không tồn tại")
           return False

     #Sign In GUI
    def signInGUI(self):
        self.master.withdraw()
        self.master1 = Toplevel(self.master)
        self.master1.title("Client") 
        self.master1.geometry("500x350") 
        self.master1.resizable(0, 0)
        Label(self.master1, text = "LIVE SCORE", fg = 'blue',font = ('Times', 30, 'bold')).pack(side = TOP, pady = 2)
        Label(self.master1, text = "SIGN IN", fg = 'blue',font = ('Times', 20)).pack(side = TOP, pady = 5)
        userLabel = Label(self.master1, text = "User Name: ", font = ('Times', 12, 'bold'))
        userLabel.pack(side = TOP, pady = 2)
        userVar = StringVar()
        userEntry = Entry(self.master1,textvariable= userVar, width = 50)
        userEntry.pack(side = TOP, pady = 2)
        passVar1 = StringVar()
        passVar2 = StringVar()
        passLabel1 = Label(self.master1, text = "Password: ",font = ('Times', 12, 'bold'))
        passLabel1.pack(side = TOP, pady = 2)
        passEntry1 = Entry(self.master1,textvariable= passVar1, show = "*", width = 50)
        passEntry1.pack(side = TOP, pady = 5)
        passLabel2 = Label(self.master1, text = "Confirm Password: ",font = ('Times', 12, 'bold'))
        passLabel2.pack(side = TOP, pady = 2)
        passEntry2 = Entry(self.master1,textvariable= passVar2, show = "*", width = 50)
        passEntry2.pack(side = TOP, pady = 5)
        self.signInFunc = partial(self.signIn1, userVar, passVar1, passVar2)
        signInButton = Button(self.master1, text = "SIGN IN", width = 10, height = 1,font = ('Times', 12, 'bold'), command = self.signInFunc)
        signInButton.pack(side = TOP, pady = 5)
        #self.master.protocol("WM_DELETE_WINDOW", self.Closing)
        self.master1.mainloop()

    #Sign In Client Confirm Func
    def signIn1(self, userVar, passVar1, passVar2):
        submittedUser = userVar.get()
        submittedPass1 = passVar1.get()
        submittedPass2 = passVar2.get()
        if (submittedPass1 != submittedPass2):
            messagebox.showwarning("Warning","Nhập mật khẩu lại không đúng")
            return False
        else:
            print("REGIST")
            sendData(self.sclient, "REGIST")
            self.signIn2(userVar, passVar1)
            return True

    #Sign In to Server Func
    def signIn2(self, userVar, passVar1):
        sendData(self.sclient, "REG")
        print("REG")
        submittedUser = userVar.get()
        print(submittedUser)
        sendData(self.sclient, submittedUser)
        submittedPass1 = passVar1.get()
        print(submittedPass1)
        sendData(self.sclient, submittedPass1)
        signal = receive(self.sclient)
        if (signal == '1'):
           messagebox.showinfo("Info", "Đăng kí thành công")
           self.master1.destroy()
           self.master.deiconify()
           return True
        else:
           messagebox.showwarning("Warning","Tên đăng nhập tồn tại")
           return False

class clientGUI(object):
    def __init__(self, master):
        self.master = master
        self.sclient = sclient
        self.master.title("Client") 
        self.master.geometry("400x200") 
        self.master.resizable(0, 0)
        Label(self.master, text = "LIVE SCORE", fg = 'blue',font = ('Times', 30, 'bold')).pack(side = TOP, pady = 2)
        Label(self.master, text = "Client", fg = 'blue',font = ('Times', 20)).pack(side = TOP, pady = 5)
        hostVar = StringVar()
        hostVar.set("Nhập IP")
        hostEntry = Entry(self.master,textvariable=hostVar, width = 50).pack(side = TOP, pady = 2)
        submittedHost = hostVar.get()
        connectFunc = partial(self.connectServer,hostVar)
        Button(self.master, text = "Connect to Server", command = connectFunc).pack(side = TOP, pady = 2)
        self.master.mainloop()

    #Connect to Server
    def connectServer(self, IPVar):
        submittedIP = IPVar.get()
        global check
        global sclient
        try:
            ADDR = (submittedIP, 65432)
            sclient.connect(ADDR)
        except Exception:
            messagebox.showerror("Error", "Chưa kết nối đến server")
            return False
        messagebox.showinfo("Info", "Kết nối đến server thành công")
        logInGUI(self.master)
        return True

        
#Main
if __name__ == "__main__":
    root = Tk()
    window = clientGUI(root)
    root.mainloop()