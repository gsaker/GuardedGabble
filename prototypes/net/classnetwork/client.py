import socket
import threading
class Server:
    def __init__(self,host,port):
        #Setting attributes
        self.host = host
        self.port = port
    def connectServer(self):
        #Create socket object and try to connect to server, if it fails then return false and print error message
        #If it succeeds then return true and print success message
        self.clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            self.clientSocket.connect((self.host,self.port))
            print("Connected to server")
            return True
        except:
            print("Connection failed")
            return False
    def recieveMessage(self):
        while True:
            receivedMessage = self.clientSocket.recv(1024)
            print("Server:",receivedMessage.decode())
    def sendMessage(self,sendData):
        self.clientSocket.send(sendData.encode())
#Setting up test variables
localhost = '127.0.0.1'
port = 64147
#Creating server object
mainServer=Server(localhost,port)
#If connection is successful then start recieve thread and start recieving messages
if mainServer.connectServer():
    receiveThread = threading.Thread(target=mainServer.recieveMessage)
    receiveThread.start()
    #Demonstration loop to keep sending messages from user input
    while True:
        message = input("Enter message:")
        mainServer.sendMessage(message)