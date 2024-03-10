import socket
from . import data
from . import encrypt
import base64
import time
import threading
import json

class Server:
    def __init__(self,serverHost,serverPort, app):
        #Setting attributes
        self.app = app
        self.serverPort = serverPort
        self.serverHost = serverHost
        self.encryptionEnabled = self.app.encryptionEnabled
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
        buffer = "" 
        while True:
            #Keep trying to recieve data from the client
            receivedData = self.socket.recv(2048).decode("utf-8")
            buffer += receivedData
            # Assuming each JSON object ends with }
            while "}" in buffer:  
                # Find the first occurrence of }
                endIndex = buffer.find("}") + 1
                # Extract the single JSON object from the buffer
                singleRequest= buffer[:endIndex]
                # Remove the processed request from the buffer
                buffer = buffer[endIndex:]  
                try:
                    #Handle the individual request
                   # receivedRequest= data.receivedData(singleRequest.encode('utf-8'))
                    #handleThread = threading.Thread(target=self.handleRequest,args=(receivedRequest,))
                    #handleThread.start()
                    receivedRequest= data.receivedData(singleRequest.encode('utf-8'))
                    self.handleRequest(receivedRequest)
                except json.JSONDecodeError as e:
                    #Print out any other JSON decode errors
                    print("JSON Decode Error:", e)
    def sendData(self,sendData):
        try:
            #This method will send a completed JSON request to the server
            self.socket.send(sendData.encode())
        except:
            print("Failed to send data")
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
        self.userID = userID
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
        if recievedPublicKey.decode('utf-8') != "None":
            print("Received public key from server")
            print("Public Key:",recievedPublicKey)
            print("UserID:",recievedUserID)
            #Send the public key to the main thread to set it in the correct person object
            self.app.recievedPublicKey(recievedUserID,recievedPublicKey)
        else:
            print("User does not have a public key on server")
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
    def messageRequest(self,messageContent, recipientID, publicKey=None):
        if self.encryptionEnabled==False:
            #This method will send a request to the server to send a message to a user
            messageRequest = data.SendData()
            #craft the request using request type 4 as described in the design section
            messageRequest.append("requestType",4)
            messageRequest.append("recipientID",recipientID)
            messageRequest.append("senderID",str(self.userID))
            messageRequest.append("messageContent",messageContent)
            messageRequest.append("username",self.app.username)
            print(recipientID)
            self.sendData(messageRequest.createJSON())
        else:
            #We have included lots of debug print statements to show 
            #the process of encrypting and decrypting messages
            print("Message:",messageContent)
            print("Recipient:",recipientID)
            #Encrypt the message using the recipient's public key
            encryptedContent = encrypt.encryptMessage(messageContent, self.app.people[recipientID].publicKey)
            if encryptedContent == False:
                self.app.showError("Encryption failed, message is too long. Please try a shorter message.")
                return
            print("Encrypted message:",encryptedContent)
            #Sign the message using the sender's private key
            signature = encrypt.signMessage(messageContent,self.app.privateKey)
            print("Signature:",signature)
            #Convert the encrypted message and signature to base64 so they can be sent in a JSON request
            encryptedContentBase64 = base64.b64encode(encryptedContent).decode('utf-8')
            signatureBase64 = base64.b64encode(signature).decode('utf-8')
            print("Encrypted message base64:",encryptedContentBase64)
            print("Signature base64:",signatureBase64)
            #Craft the request using request type 4 as described in the design section
            messageRequest = data.SendData()
            messageRequest.append("requestType",4)
            messageRequest.append("recipientID",recipientID)
            messageRequest.append("senderID",self.userID)
            messageRequest.append("messageContent",encryptedContentBase64)
            messageRequest.append("signature",signatureBase64)
            messageRequest.append("username",self.app.username)
            # For now we will send the sender public key with the message request 
            #but in the future this will be requested from the server for security reasons
            #messageRequest.append("senderPublicKey",publicKey.decode('utf-8'))
            print("Sending message request")
            self.sendData(messageRequest.createJSON())

    def handleMessageResponse(self,receivedRequest):
        if receivedRequest.get("senderID") not in self.app.people:
            print("Adding new person to people list")
            self.app.addPerson(str(receivedRequest.get("senderID")), str(receivedRequest.get("senderID")))
        if self.encryptionEnabled==False:
            #specific handler for a message response from the server
            #prints out the message content and the sender
            self.app.people[str(receivedRequest.get("senderID"))].setUsername(receivedRequest.get("username"))
            self.app.receivedMessage(receivedRequest.get("senderID"),receivedRequest.get("messageContent"))
        else:
            #We have included lots of debug print statements to show whats going on
            encryptedContentBase64 = receivedRequest.get("messageContent")
            signatureBase64 = receivedRequest.get("signature")
            #Convert the base64 encoded encrypted message and signature back to bytes
            encryptedContent = base64.b64decode(encryptedContentBase64)
            signature = base64.b64decode(signatureBase64)
            print("Received encrypted message:",encryptedContent)
            print("Received signature:",signature)
            #Decrypt the message using the recipient's private key
            decryptedContent = encrypt.decryptMessage(encryptedContent,self.app.privateKey)
            print("Decrypted message:",decryptedContent)
            print("Verifying signature")
            senderPublicKey = receivedRequest.get("senderPublicKey").encode('utf-8')
            self.app.people[str(receivedRequest.get("senderID"))].publicKey = senderPublicKey
            self.app.people[str(receivedRequest.get("senderID"))].setUsername(receivedRequest.get("username"))
            #Verify the signature using the sender's public key
            verified = encrypt.verifySignature(decryptedContent,signature,senderPublicKey)
            print("Signature verified:",verified)
            # If the signature is verified then print out the message content and the sender
            if verified:
                self.app.receivedMessage(str(receivedRequest.get("senderID")),decryptedContent.decode('utf-8'))
            # Otherwise the message may have been tampered with
            else:
                print("Signature not verified")