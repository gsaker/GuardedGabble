import socket
from . import data
class Server:
    def __init__(self,serverHost,serverPort, app):
        #Setting attributes
        self.app = app
        self.serverPort = serverPort
        self.serverHost = serverHost
    def connectServer(self):
        #Create socket object and try to connect to server, if it fails then return false and print error message
        #If it succeeds then return true and print success message
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.socket.connect((self.serverHost,self.serverPort))
            print("Connected to server")
            return True
        except:
            print("Connection failed")
            return False
    def recieveMessage(self):
        #This will run in a seperate thread, loop forever and try and recieve data from the server
        while True:
            recievedRequest = data.RecievedData(self.socket.recv(1024))
            self.handleRequest(recievedRequest)
    def sendData(self,sendData):
        #This method will send a completed JSON request to the server
        self.socket.send(sendData.encode())
    def newUserRequest(self,username):
        #This method will send a request to the server to create a new user
        print("Sending request for userID")
        userIDRequest = data.SendData()
        #craft the request using request type 0 as described in the design section
        userIDRequest.append("requestType",0)
        userIDRequest.append("username",username)
        self.sendData(userIDRequest.createJSON())
    def handleRequest(self,recievedRequest):
        #Main handler method for when data is recieved from the server
        #This will be added to later as more request types are added
        requestType = recievedRequest.get("requestType")
        if requestType == 1:
            self.handleNewUserResponse(recievedRequest)
        if requestType == 4:
            self.handleMessageResponse(recievedRequest)
    def handleNewUserResponse(self,recievedRequest):
        #specific handler for a new user response from the server
        #sets userID sent by the server
        self.userID = recievedRequest.get("userID")
        print("Recieved userID from server")
        print("UserID:",self.userID)
    def messageRequest(self,messageContent, recipientID):
        #This method will send a request to the server to send a message to a user
        messageRequest = data.SendData()
        #craft the request using request type 2 as described in the design section
        messageRequest.append("requestType",4)
        messageRequest.append("recipientID",recipientID)
        messageRequest.append("senderID",self.userID)
        messageRequest.append("messageContent",messageContent)
        print(recipientID)
        self.sendData(messageRequest.createJSON())
    def handleMessageResponse(self,recievedRequest):
        #specific handler for a message response from the server
        #prints out the message content and the sender
        # print("Message from:",recievedRequest.get("senderID"))
        # print("Message:",recievedRequest.get("messageContent"))
        self.app.recievedMessage(recievedRequest.get("senderID"),recievedRequest.get("messageContent"))