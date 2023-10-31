import socket
import threading
from net import *
import random
def startServer(host,port):
    serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    serverSocket.bind((host,port))
    serverSocket.listen(5)
    allClients = client.Clients()
    #This creates new client objects for each client that connects
    #Each client object will in the future be stored in a dictionary with userIDs as keys
    while True:
        clientSocket, clientAddress= serverSocket.accept()
        userID = random.randint(100000,999999)
        newClient = client.Client(clientSocket,clientAddress,userID)
        allClients.addClient(newClient)
        receiveThread = threading.Thread(target=newClient.recieveMessage)
        receiveThread.start()
localhost = '127.0.0.1'
port = 64147
acceptClients = threading.Thread(target=startServer,args=(localhost,port))
acceptClients.start()
print("Done")