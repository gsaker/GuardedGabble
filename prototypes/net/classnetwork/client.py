import socket
import threading
class Server:
    def __init__(self,serverName):
        self.serverName = serverName
        self.port = 64148
        self.connectServer(serverName)
    def connectServer(self,serverName):
        self.clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            self.clientSocket.connect((self.serverName,self.port))
        except:
            print("Connection refused")
    def recieveMessage(self):
        while True:
            recievedMessage = self.clientSocket.recv(1024)
            print("Server:",recievedMessage.decode())
    def sendMessage(self,sendData):
        self.clientSocket.send(sendData.encode())
mainServer=Server('127.0.0.1')
receiveThread = threading.Thread(target=mainServer.recieveMessage)
receiveThread.start()
