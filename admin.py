import socket
import json

hostname = socket.gethostname()
HOST = socket.gethostbyname(hostname) 
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

def login(sock):
    u = input('Username: ')
    sendData(sock, u)
    p = input('Password: ')
    sendData(sock, p)
    data = receive(sock)
    if (data == '1'):
        print('Đăng nhập thành công')
        return True
    else:
        print('Tài khoản admin không đúng')
        return False

def addEvent(sock):
    # type(data) = dict, data = {"id": <match's id>, "events":[<only one event>]} 
    data = {"id": "1234", "events" : [ { "time": "FT", "score": "2-0"} ] }
    sendData(sock, json.dumps(data))
    res = receive(sock)
    if (res == '1'):
        print('Thêm sự kiện thành công')
    else:
        print('Thêm sự kiện không thành công')

def addMatch(sock):
    # type(data) = dict, data = {"id", "team1", "team2", "time", "score"}
    data = {"id": "1235", "team1": "MU", "team2": "Liverpool", "time": "FT", "score": "3-0" }
    sendData(sock, json.dumps(data))
    res = receive(sock)
    if (res == '1'):
        print('Thêm trận đấu thành công')
    else:
        print('Thêm trận đấu không thành công')

def updMatch(sock, mode):   # mode 0: update score, mode 1: update time
    # type(data) = dict, data = {"id", "score"/"time"}
    data = {"id": "1234", "time": "80"}
    sendData(sock, json.dumps(data))
    res = receive(sock)
    if (res == '1'):
        print('Cập nhật thành công')
    else:
        print('Cập nhật không thành công')

def updEvent(sock):
    # type(data) = dict, data = {"eventID" = <type int, index of the updated event in match's events list>, 
    #                            "matchID", "event"}
    data = {"eventID": 0, "matchID": "1234", "event": {"time": "14", "type": "goalPen", "team": "MU", "player": "Bruno", "score": "1-0"} }
    sendData(sock, json.dumps(data))
    res = receive(sock)
    if (res == '1'):
        print('Cập nhật thành công')
    else:
        print('Cập nhật không thành công')
    pass

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sAdmin:
    server_address = (HOST, PORT)
    print("Client connect to server with port: " + str(PORT))
    sAdmin.connect(server_address)
    try:
        while True:
            msg = input('Client: ')
            sendData(sAdmin, msg)

            if (msg == "ADLOG"):
                msg = input('Client: ')
                sendData(sAdmin, msg)
                if (msg == "LOG"):
                    checkAd = login(sAdmin)

                while checkAd:
                    msg = input('Client: ')
                    sendData(sAdmin, msg)
                    if (msg == "ADDEV"):
                        msg = input('Client: ')
                        sendData(sAdmin, msg)
                        if (msg == "ADD"):
                            addEvent(sAdmin)
                    
                    elif (msg == "ADDMT"):
                        msg = input('Client: ')
                        sendData(sAdmin, msg)
                        if (msg == "ADD"):
                            addMatch(sAdmin)
                    
                    elif (msg == "UPDSC"):
                        msg = input('Client: ')
                        sendData(sAdmin, msg)
                        if (msg == "UPD"):
                            updMatch(sAdmin, 0)

                    elif (msg == "UPDTM"):
                        msg = input('Client: ')
                        sendData(sAdmin, msg)
                        if (msg == "UPD"):
                            updMatch(sAdmin, 1)

                    elif (msg == "UPDEV"):
                        msg = input('Client: ')
                        sendData(sAdmin, msg)
                        if (msg == "UPD"):
                            updEvent(sAdmin)
                    
                    else:
                        checkAd = False
                        break

            else:
                break
            
    except KeyboardInterrupt:
        sAdmin.close()
    finally:
        sAdmin.close()