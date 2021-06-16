
import socket
import subprocess
import sys
import os
import time

#class Cleint:
#    def __init__(self):
#        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#        self.connection = None



black   = "u001b[30m"
red     = "u001b[31m"
green   = "u001b[32m"
yellow  = "u001b[33m"
blue    = "u001b[34m"
white   = "u001b[37m"

soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
soc.connect(("127.0.0.1",8080))
while True:
    try:
        command = input("$ ").lower()
        cmd = command.split(' ')
        if command=="":continue
        elif cmd[1] in ["quit","q","exit","e"]:
            print("Bye!")
            break
        elif cmd[1]=='clear':
            x=os.system('clear')
        elif cmd[1] == "download":
            output = input("Output path : ")
            file_name = command.split(' ')[1]
            full_path = os.path.join(output,file_name)
            res = soc.send(command.encode())
            with open(full_path,"wb") as file:
                data = ' '
                try:
                    while 1:
                        
                        if data: 
                            data = soc.recv(1024)
                            file.write(data)
                        else:
                            break
                except KeyboardInterrupt:
                    pass
                print("[+]",data[:20],"\n")
                file.close
        elif command.lower()=="upload":
            file_name = cmd[1]

        else:
            res = soc.send(command.encode())
            res = soc.recv(1024).decode()
            print("\n".join(res.split("\\n")))
            sys.stdout.flush()
    except KeyboardInterrupt:
        print(f"\nError: Type Quit/quit to exit the program!")