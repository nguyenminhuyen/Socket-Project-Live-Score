from tkinter import *
from tkinter import ttk
from PIL import ImageTk,Image
from tkinter import messagebox
from tkinter import filedialog
from functools import partial
from socket import AF_INET, socket, SOCK_STREAM
import json
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


class adminGUI(object):
    def __init__(self,master):
        self.master = Toplevel(master)
        self.sclient = sclient
        self.master.title("Client admin") 
        self.master.geometry("500x350") 
        self.master.resizable(0, 0)
        Label(self.master, text = "LIVE SCORE", fg = 'blue',font = ('Times', 30, 'bold')).pack(side = TOP, pady = 2)
        Label(self.master, text = "ADMIN", fg = 'blue',font = ('Times', 20)).pack(side = TOP, pady = 7)
        Button(self.master, text = "Thêm trận", height = 2, width = 30, command = self.addMatchGUI).pack(side = TOP, pady = 2)
        Button(self.master, text = "Cập nhật thời gian và tỉ số", height = 2, width = 30, command = self.upMatchGUI).pack(side = TOP, pady = 2)
        Button(self.master, text = "Cập nhật event", height = 2, width = 30, command = self.upEventGUI).pack(side = TOP, pady = 2)
        self.master.mainloop()

    #Add Match
    def addMatchGUI(self):
        self.master1 = Toplevel(self.master)
        self.master1.title("ADD SCORE") 
        self.master1.geometry("500x350") 
        self.master1.resizable(0, 0)
        #Nhập ID
        IDLabel = Label(self.master1, text = "Nhập ID: ", font = ('Times', 12, 'bold'))
        IDLabel.pack(side = TOP, pady = 2)
        IDVar = StringVar()
        IDEntry = Entry(self.master1,textvariable= IDVar, width = 50, bg = "white")
        IDEntry.pack(side = TOP, pady = 2)

        #Nhập time
        timeVar = StringVar()
        timeLabel = Label(self.master1, text = "Nhập time: ",font = ('Times', 12, 'bold'))
        timeLabel.pack(side = TOP, pady = 2)
        timeEntry = Entry(self.master1,textvariable= timeVar, width = 50, bg = "white")
        timeEntry.pack(side = TOP, pady = 5)

        #Nhập team1
        team1Var = StringVar()
        team1Label = Label(self.master1, text = "Nhập tên đội: ",font = ('Times', 12, 'bold'))
        team1Label.pack(side = TOP, pady = 2)
        team1Entry = Entry(self.master1,textvariable= team1Var, width = 50, bg = "white")
        team1Entry.pack(side = TOP, pady = 5)

        #Nhập team2
        team2Var = StringVar()
        team2Label = Label(self.master1, text = "Nhập tên đội: ",font = ('Times', 12, 'bold'))
        team2Label.pack(side = TOP, pady = 2)
        team2Entry = Entry(self.master1,textvariable= team2Var, width = 50, bg = "white")
        team2Entry.pack(side = TOP, pady = 5)

        #Nhập tỉ số 
        scoreVar = StringVar()
        scoreLabel = Label(self.master1, text = "Nhập tỉ số: ",font = ('Times', 12, 'bold'))
        scoreLabel.pack(side = TOP, pady = 2)
        scoreEntry = Entry(self.master1,textvariable= scoreVar, width = 50, bg = "white")
        scoreEntry.pack(side = TOP, pady = 5)

        #Button
        self.addMatchFunc = partial(self.addMatch, IDVar, timeVar, team1Var, team2Var, scoreVar)
        addMatchButton = Button(self.master1, text = "ADD MATCH", width = 12, height = 1,font = ('Times', 12, 'bold'), command = self.addMatchFunc)
        addMatchButton.pack(side = TOP, pady = 5)
        self.master1.mainloop()

    def addMatch(self, IDVar, timeVar, team1Var, team2Var, scoreVar):
        sendData(self.sclient, "ADDMT")
        #type(str) = dict
        str = {"id": IDVar.get(), "time": team1Var.get(), "team1": team1Var.get(),"score": scoreVar.get(), "team2": team2Var.get()}
        sendData(self.sclient,json.dumps(str))
        signal = receive(self.sclient)
        if (signal == '0'):
            messagebox.showinfo("Info", "Thêm trận đấu không thành công")
            return False
        else:
            messagebox.showinfo("Info", "Thêm trận đấu thành công")
            return True

    #Update Match
    def upMatchGUI(self):
        self.master1 = Toplevel(self.master)
        self.master1.title("UPDATE MATCH") 
        self.master1.geometry("500x350") 
        self.master1.resizable(0, 0)
        #Nhập ID
        IDLabel = Label(self.master1, text = "Nhập ID: ", font = ('Times', 12, 'bold'))
        IDLabel.pack(side = TOP, pady = 2)
        IDVar = StringVar()
        IDEntry = Entry(self.master1,textvariable= IDVar, width = 50, bg = "white")
        IDEntry.pack(side = TOP, pady = 2)

        #Nhập time
        timeVar = StringVar()
        timeLabel = Label(self.master1, text = "Nhập time: ",font = ('Times', 12, 'bold'))
        timeLabel.pack(side = TOP, pady = 2)
        timeEntry = Entry(self.master1,textvariable= timeVar, width = 50, bg = "white")
        timeEntry.pack(side = TOP, pady = 5)

        #Nhập tỉ số 
        scoreVar = StringVar()
        scoreLabel = Label(self.master1, text = "Nhập tỉ số: ",font = ('Times', 12, 'bold'))
        scoreLabel.pack(side = TOP, pady = 2)
        scoreEntry = Entry(self.master1,textvariable= scoreVar, width = 50, bg = "white")
        scoreEntry.pack(side = TOP, pady = 5)

        #Button
        self.upMatchFunc = partial(self.upMatch, IDVar, timeVar, scoreVar)
        upMatchButton = Button(self.master1, text = "UPDATE MATCH", width = 15, height = 1,font = ('Times', 12, 'bold'), command = self.upMatchFunc)
        upMatchButton.pack(side = TOP, pady = 5)
        self.master1.mainloop()
    
    def upMatch(self, IDVar, timeVar, scoreVar):
        sendData(self.sclient, "UPDMT")
        str = {"id": IDVar.get(), "time": timeVar.get(), "score": scoreVar.get()}
        sendData(self.sclient,json.dumps(str))
        signal = receive(self.sclient)
        if (signal == '0'):
            messagebox.showinfo("Info", "Cập nhật trận đấu không thành công")
            return False
        else:
            messagebox.showinfo("Info", "Cập nhật trận đấu thành công")
            return True

    #Update Event
    def upEventGUI(self):
        self.master1 = Toplevel(self.master)
        self.master1.title("UPDATE EVENT") 
        self.master1.geometry("500x500") 
        self.master1.resizable(0, 0)
        
        #Nhập ID Match
        IDMLabel = Label(self.master1, text = "Nhập ID: ", font = ('Times', 12, 'bold'))
        IDMLabel.pack(side = TOP, pady = 2)
        IDMVar = StringVar()
        IDMEntry = Entry(self.master1,textvariable= IDMVar, width = 50, bg = "white")
        IDMEntry.pack(side = TOP, pady = 2)

        #Nhập time
        timeVar = StringVar()
        timeLabel = Label(self.master1, text = "Nhập time: ",font = ('Times', 12, 'bold'))
        timeLabel.pack(side = TOP, pady = 2)
        timeEntry = Entry(self.master1,textvariable= timeVar, width = 50, bg = "white")
        timeEntry.pack(side = TOP, pady = 5)

        #Nhập team
        teamVar = StringVar()
        teamLabel = Label(self.master1, text = "Nhập tên đội: ",font = ('Times', 12, 'bold'))
        teamLabel.pack(side = TOP, pady = 2)
        teamEntry = Entry(self.master1,textvariable= teamVar, width = 50, bg = "white")
        teamEntry.pack(side = TOP, pady = 5)

        #Nhập type
        typeLabel = Label(self.master1, text = "Nhập loại sự kiện: ",font = ('Times', 12, 'bold'))
        typeLabel.pack(side = TOP, pady = 2)
        self.choosenTypes = ["goal", "goalPen", "RedCard", "YellowCard"]
        self.typeVar = StringVar()
        self.TypeChoosen = ttk.Combobox(self.master1, value = self.choosenTypes, textvariable = self.typeVar)
        self.TypeChoosen.pack(side = TOP, pady = 2)
        self.TypeChoosen.bind("<<ComboboxSelected>>", self.option)
        
        self.topFrame = Frame(self.master1)
        self.topFrame.pack(side = TOP, pady = 2 )
        #Nhập player
        playerVar = StringVar()
        self.playerLabel = Label(self.topFrame, text = "Nhập player: ",font = ('Times', 12, 'bold'))
        self.playerLabel.pack(side = TOP, pady = 2)
        self.playerEntry = Entry(self.topFrame,textvariable= playerVar, width = 50, bg = "white")
        self.playerEntry.pack(side = TOP, pady = 5)

        #Nhập assist
        assistVar = StringVar()
        self.assistLabel = Label(self.topFrame, text = "Nhập assist: ",font = ('Times', 12, 'bold'))
        self.assistLabel.pack(side = TOP, pady = 2)
        self.assistEntry = Entry(self.topFrame,textvariable= assistVar, width = 50, bg = "white")
        self.assistEntry.pack(side = TOP, pady = 5)

        #Nhập tỉ số 
        scoreVar = StringVar()
        self.scoreLabel = Label(self.topFrame, text = "Nhập tỉ số: ",font = ('Times', 12, 'bold'))
        self.scoreLabel.pack(side = TOP, pady = 2)
        self.scoreEntry = Entry(self.topFrame,textvariable= scoreVar, width = 50, bg = "white")
        self.scoreEntry.pack(side = TOP, pady = 5)
        
        #Button
        self.bottomFrame = Frame(self.master1)
        self.bottomFrame.pack(side = TOP, pady = 2 )
        self.upEventFunc = partial(self.upEvent, IDMVar, timeVar, teamVar, playerVar, assistVar, scoreVar)
        self.upEventButton = Button(self.bottomFrame, text = "UP EVENT", width = 12, height = 1,font = ('Times', 12, 'bold'), command = self.upEventFunc)
        self.upEventButton.pack(side = TOP, pady = 5)
        self.master1.mainloop()
    
    def upEvent(self, IDMVar, timeVar, teamVar, playerVar, assistVar, scoreVar):
        sendData(self.sclient, "UPDEV")
        print("UPDEV")
        print(IDMVar.get() + "\n")
        print(teamVar.get() + "\n")
        print(playerVar.get() + "\n")
        print(scoreVar.get() + "\n")
        assist = assistVar.get()
        if (assist == None):
            assist = ""
        print(assist + "\n")
        str = {"id": IDMVar.get(), "events": {"time": timeVar.get(), "type": self.TypeChoosen.get(), "team": teamVar.get(), "player": playerVar.get(), "assist": assist, "score": scoreVar.get()} }
        sendData(self.sclient,json.dumps(str))
        signal = receive(self.sclient)
        print(signal)
        if (signal == '0'):
            messagebox.showinfo("Info", "Cập nhật sự kiện không thành công")
            return False
        else:
            messagebox.showinfo("Info", "Cập nhật sự kiện thành công")
            return True

    def option(self, event):
        ch = self.TypeChoosen.get()
        if (ch == self.choosenTypes[0]):
            self.assistLabel.pack(side = TOP, pady = 2)
            self.assistEntry.pack(side = TOP, pady = 5)
            self.scoreLabel.pack(side = TOP, pady = 2)
            self.scoreEntry.pack(side = TOP, pady = 5)
        else:
            self.assistLabel.pack(side = TOP, pady = 2)
            self.assistEntry.pack(side = TOP, pady = 5)
            self.scoreLabel.pack(side = TOP, pady = 2)
            self.scoreEntry.pack(side = TOP, pady = 5)
            self.assistLabel.pack_forget()
            self.assistEntry.pack_forget()
        return

class userGUI(object):
    def __init__(self, master):
        self.master = Toplevel(master)
        self.master.title("DANH SÁCH TRẬN ĐẤU") 
        self.master.geometry("700x400") 
        self.master.resizable(0, 0)
        self.sclient = sclient
        Label(self.master, text = "LIVE SCORE", fg = 'blue',font = ('Times', 30, 'bold')).pack(side = TOP, pady = 2)
        Label(self.master, text = "LIST SCORE", fg = 'blue',font = ('Times', 20)).pack(side = TOP, pady = 5)
        Button(self.master, text = "Hiển thị danh sách trận đấu", command = self.listMatch).pack(side = TOP, pady = 5)
        self.topFrame = Frame(self.master)
        self.topFrame.pack(side = TOP, pady = 2, padx = 5)
        Label(self.topFrame, text = "Match detail", font = ('Time', 11, 'bold')).pack(side = LEFT, padx = 2)
        self.IDMVar = StringVar()
        self.IDMVar.set("Nhập ID Match")
        IDMEntry = Entry(self.topFrame,textvariable= self.IDMVar, width = 50).pack(side = LEFT, padx = 2)
        Button(self.topFrame, text = "Xem", command = self.matchDetailGUI).pack(side = LEFT)
        self.bottomFrame = Frame(self.master)
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
        self.master.mainloop()

    def listMatch(self):
        sendData(self.sclient, "LISTMT")
        print("LISTMT")
        mtchs =[]
        while True:
            data = receive(sclient)
            if (data == '0'):
                break
            data = json.loads(data)
            print(data)
            mtchs.append(data)
        cnt = 0
        for mtch in mtchs:
            self.treev.insert("", 'end', iid = cnt, text ="", values =(mtch['id'], mtch['time'], mtch['team1'], mtch['score'], mtch['team2']))
            cnt += 1
        return

    def matchDetailGUI(self):
        self.master1 = Toplevel(self.master)
        self.master1.title("DANH SÁCH TRẬN ĐẤU") 
        self.master1.geometry("700x400") 
        self.master1.resizable(0, 0)
        Label(self.master1, text = "LIVE SCORE", fg = 'blue',font = ('Times', 30, 'bold')).pack(side = TOP, pady = 2)
        Label(self.master1, text = "LIST SCORE", fg = 'blue',font = ('Times', 20)).pack(side = TOP, pady = 5)
        Button(self.master1, text = "Hiển thị danh sách sự kiện", command = self.matchDetail).pack(side = TOP, pady = 5)
        self.bottomFrame = Frame(self.master1)
        self.bottomFrame.pack(side = TOP, fill = X )
        self.treev1 = ttk.Treeview(self.bottomFrame, selectmode ='browse')
        self.treev1.pack(side =TOP)
        verscrlbar = ttk.Scrollbar(self.bottomFrame, orient ="vertical", command = self.treev1.yview)
        verscrlbar.pack(side ='right', fill ='x')
        self.treev1.configure(xscrollcommand = verscrlbar.set)
        self.treev1["columns"] = ("1", "2", "3", "4", "5", "6", "7")
        self.treev1['show'] = 'headings'
        self.treev1.column("1", width = 100, anchor ='c')
        self.treev1.column("2", width = 100, anchor ='se')
        self.treev1.column("3", width = 100, anchor ='se')
        self.treev1.column("4", width = 100, anchor ='se')
        self.treev1.column("5", width = 100, anchor ='se')
        self.treev1.column("6", width = 100, anchor ='se')
        self.treev1.column("7", width = 100, anchor ='se')
        self.treev1.heading("1", text ="ID Match")
        self.treev1.heading("2", text ="Time")
        self.treev1.heading("3", text ="Type")
        self.treev1.heading("4", text = "Team")
        self.treev1.heading("5", text = "Player")
        self.treev1.heading("6", text = "Assist")
        self.treev1.heading("7", text = "Score")
        self.master1.mainloop()

    def matchDetail(self):
        sendData(self.sclient, "MTCDT")
        IDM = self.IDMVar.get()
        sendData(self.sclient, IDM)
        mtchs = []
        while True:
            data = receive(sclient)
            if (data == '0'):
                break
            data = json.loads(data)
            print(data)
            mtchs.append(data)
        cnt = 0
        for mtch in mtchs:
            self.treev.insert("", 'end', iid = cnt, text ="", values =(mtch['id'], mtch['time'], mtch['type'], mtch['team'], mtch['player'], mtch['assist'], mtch['score']))
            cnt += 1
        return
        
class logInGUI(object):

    #Log In GUI
    def __init__(self, master):
        master.withdraw()
        self.master = Toplevel(master)
        self.sclient = sclient
        self.master.title("Client") 
        self.master.geometry("500x350") 
        self.master.resizable(0, 0)
        self.img = Image.open("gui.jpg")
        img1 = self.img.resize((500, 350), Image.ANTIALIAS)
        self.bg=ImageTk.PhotoImage(img1)
        self.bg_image=Label(self.master,image=self.bg).place(x=0,y=0,relwidth=1,relheight=1)
        Label(self.master, text = "LIVE SCORE", fg = 'blue',font = ('Times', 30, 'bold')).pack(side = TOP, pady = 2)
        Label(self.master, text = "LOG IN", fg = 'blue',font = ('Times', 20)).pack(side = TOP, pady = 5)
        userLabel = Label(self.master, text = "User Name: ", font = ('Times', 12, 'bold'))
        userLabel.pack(side = TOP, pady = 2)
        self.userVar = StringVar()
        userEntry = Entry(self.master,textvariable= self.userVar, width = 50, bg = "white")
        userEntry.pack(side = TOP, pady = 2)
        self.passVar = StringVar()
        passLabel = Label(self.master, text = "Password: ",font = ('Times', 12, 'bold'))
        passLabel.pack(side = TOP, pady = 2)
        passEntry = Entry(self.master,textvariable= self.passVar,show = "*", width = 50, bg = "white")
        passEntry.pack(side = TOP, pady = 5)
        #logInFunc = partial(self.logIn, self.userVar, self.passVar)
        logInButton = Button(self.master, text = "LOG IN", width = 10, height = 1,font = ('Times', 12, 'bold'), command = self.logIn)
        logInButton.pack(side = TOP, pady = 5)
        signInLabel = Label(self.master, text = "Nếu bạn chưa có tài khoản", font = ('Times', 12, 'italic')).pack(side = TOP, pady = 5)
        signInButton = Button(self.master, text = "SIGN IN", width = 10, height = 1, font = ('Times', 12, 'bold'), command = self.signInGUI)
        signInButton.pack(side = TOP)
        #self.master.protocol("WM_DELETE_WINDOW", self.Closing)
        self.master.mainloop()

    #Log In Func
    def logIn(self):
        print("LOGIN")
        sendData(self.sclient, "LOGIN")
        str = {"usr": self.userVar.get(), "psw": self.passVar.get()}
        sendData(self.sclient,json.dumps(str))
        print(self.userVar.get())
        print(self.passVar.get())
        signal = receive(self.sclient)
        if (signal == '2'):
            messagebox.showinfo("Info", "Đăng nhập admin thành công")
            adminGUI(self.master)
            return True
        elif (signal == '1'):
           messagebox.showinfo("Info", "Đăng nhập thành công")
           userGUI(self.master)
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
        self.userVar1 = StringVar()
        userEntry = Entry(self.master1,textvariable= self.userVar1, width = 50)
        userEntry.pack(side = TOP, pady = 2)
        self.passVar1 = StringVar()
        self.passVar2 = StringVar()
        passLabel1 = Label(self.master1, text = "Password: ",font = ('Times', 12, 'bold'))
        passLabel1.pack(side = TOP, pady = 2)
        passEntry1 = Entry(self.master1,textvariable= self.passVar1, show = "*", width = 50)
        passEntry1.pack(side = TOP, pady = 5)
        passLabel2 = Label(self.master1, text = "Confirm Password: ",font = ('Times', 12, 'bold'))
        passLabel2.pack(side = TOP, pady = 2)
        passEntry2 = Entry(self.master1,textvariable= self.passVar2, show = "*", width = 50)
        passEntry2.pack(side = TOP, pady = 5)
        self.signInFunc = partial(self.signIn1)
        signInButton = Button(self.master1, text = "SIGN IN", width = 10, height = 1,font = ('Times', 12, 'bold'), command = self.signInFunc)
        signInButton.pack(side = TOP, pady = 5)
        #self.master.protocol("WM_DELETE_WINDOW", self.Closing)
        self.master1.mainloop()

    #Sign In Client Confirm Func
    def signIn1(self):
        if (self.passVar1.get() != self.passVar2.get()):
            messagebox.showwarning("Warning","Nhập mật khẩu lại không đúng")
            return False
        else:
            self.signIn2()
            return True

    #Sign In to Server Func
    def signIn2(self):
        sendData(self.sclient, "REGIST")
        print("REGIST")
        str = {"usr": self.userVar1.get(), "psw": self.passVar1.get()}
        sendData(self.sclient,json.dumps(str))
        print(self.userVar.get())
        print(self.passVar.get())
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