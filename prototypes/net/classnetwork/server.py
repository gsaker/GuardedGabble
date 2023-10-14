import socket
import threading
#Each client will have its own object
class Client:
    def __init__(self,socket,host):
        #Setting attributes
        self.socket = socket
        self.host = host
    def recieveMessage(self):
        while True:
            recievedMessage = self.socket.recv(1024)
            print("Client:",recievedMessage.decode())
    def sendMessage(self,sendData):
        self.clientSocket.send(sendData.encode())

def startServer(host,port):
    serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    serverSocket.bind((host,port))
    serverSocket.listen(5)
    #This creates new client objects for each client that connects
    #Each client object will in the future be stored in a dictionary with userIDs as keys
    while True:
        clientSocket, clientAddress= serverSocket.accept()
        newClient = Client(clientSocket,clientAddress)
        receiveThread = threading.Thread(target=newClient.recieveMessage)
        receiveThread.start()
#Setting up test variables
localhost = '127.0.0.1'
port = 64147
startServer(localhost,port)

