from . import data
class Clients:
    def __init__(self):
        self.clients = {}
    def addClient(self,client):
        self.clients[client.host] = client
    def removeClient(self,client):
        self.clients.pop(client.host)
    def sendMessage(self,sendData,userID):
        self.clients[userID].sendMessage(sendData)

class Client:
    def __init__(self,socket,host,userID):
        #Setting attributes
        self.socket = socket
        self.host = host
        self.username = ""
        self.userID = userID
    def recieveMessage(self):
        while True:
            recievedRequest = data.RecievedData(self.socket.recv(1024))
            self.handleRequest(recievedRequest)
    def sendMessage(self,sendData):
        self.socket.send(sendData.encode())
    def handleRequest(self,recievedRequest):
        requestType = recievedRequest.get("requestType")
        if requestType == 0:
            self.handleNewUser(recievedRequest)
    def handleNewUser(self,recievedRequest):
        self.username = recievedRequest.get("username")
        print("New User Connected!")
        print("Host:",self.host)
        print("UserID:",self.userID)
        print("Username:",self.username)
        self.newUserResponse()
    def newUserResponse(self):
        userIDResponse = data.SendData()
        userIDResponse.append("requestType",1)
        userIDResponse.append("userID",self.userID)
        self.sendMessage(userIDResponse.createJSON())
        


            

