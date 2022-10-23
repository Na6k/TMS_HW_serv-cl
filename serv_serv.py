import socket
import select
from abc import ABC, abstractmethod


class ServerObj(ABC):

    HOST = "127.0.0.1"
    PORT = 5678
    FOR_READ = []

    def create_serv(self):
        self.serv_serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serv_serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serv_serv.setblocking(False)
        self.serv_serv.bind((self.HOST, self.PORT))
        self.serv_serv.listen(1000)

    def create_client(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.HOST, self.PORT))

    @abstractmethod
    def run(self):
        ...


class Server(ServerObj):
    def run(self):
        while True:
            R, _, _ = select.select(self.FOR_READ + [self.serv_serv], [], [])
            for r in R:
                if r is not self.serv_serv:
                    try:
                        data = r.recv(2**16)
                    except ConnectionRefusedError:
                        r.close()
                    else:
                        data = data.decode("utf-8")
                        for message in self.FOR_READ:
                            if message is not r:
                                message.send(data.encode("utf-8"))
                else:
                    self.client, addr = self.serv_serv.accept()
                    self.client.setblocking(False)
                    print(addr)
                    self.FOR_READ.append(self.client)

    # def __str__(self):
    #    return  self.client


class Client(ServerObj):
    def run(self):
        run = True
        while run:
            mod = input("change mod: write/read/CLOSE ")
            if mod == "write":
                mess = input("write your message: ")
                self.client.send(mess.encode("utf-8"))
            elif mod == "read":
                response = self.client.recv(2**16)
                print(response.decode("utf-8"))
            elif mod == "CLOSE":
                run = False
