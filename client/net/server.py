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
            receivedRequest = data.receivedData(self.socket.recv(1024))
            self.handleRequest(receivedRequest)
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
    def setUserIDRequest(self,userID):
        print("Sending request to set userID to stored value")
        userIDRequest = data.SendData()
        #craft the request using request type 5
        userIDRequest.append("requestType",5)
        userIDRequest.append("userID",userID)
        self.sendData(userIDRequest.createJSON())
    def setPublicKeyRequest(self,publicKey):
        print("Sending request to set public key")
        publicKeyRequest = data.SendData()
        #craft the request using request type 6
        publicKeyRequest.append("requestType",6)
        #Need to convert to string to store in JSON
        publicKeyRequest.append("publicKey",publicKey.decode('utf-8'))
        self.sendData(publicKeyRequest.createJSON())
    def getPublicKeyRequest(self,userID):
        print("Sending request to get public key")
        publicKeyRequest = data.SendData()
        #craft the request using request type 2
        #See design document for more information
        publicKeyRequest.append("requestType",2)
        publicKeyRequest.append("userID",userID)
        self.sendData(publicKeyRequest.createJSON())
    def handleGetPublicKeyResponse(self,receivedRequest):
        #Extract the relevant data from the received request and print it out
        #Need to convert to bytes to use in encryption
        recievedPublicKey = receivedRequest.get("publicKey").encode('utf-8')
        recievedUserID = receivedRequest.get("userID")
        print("Received public key from server")
        print("Public Key:",recievedPublicKey)
        print("UserID:",recievedUserID)
        #Send the public key to the main thread to set it in the correct person object
        self.app.recievedPublicKey(recievedUserID,recievedPublicKey)

    def handleRequest(self,receivedRequest):
        #Main handler method for when data is received from the server
        #This will be added to later as more request types are added
        requestType = receivedRequest.get("requestType")
        if requestType == 1:
            self.handleNewUserResponse(receivedRequest)
        if requestType == 3:
            self.handleGetPublicKeyResponse(receivedRequest)
        if requestType == 4:
            self.handleMessageResponse(receivedRequest)
    def handleNewUserResponse(self,receivedRequest):
        #specific handler for a new user response from the server
        #sets userID sent by the server
        self.userID = receivedRequest.get("userID")
        print("received userID from server")
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
    def handleMessageResponse(self,receivedRequest):
        #specific handler for a message response from the server
        #prints out the message content and the sender
        self.app.receivedMessage(receivedRequest.get("senderID"),receivedRequest.get("messageContent"))