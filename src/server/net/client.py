from . import data
from data import person
import sys
import time
import json
import threading
sys.path.append(".")

class Clients:
    #This class will hold all the clients connected to the server
    #Clients can only be added or removed from this class due to the attribute being private
    #This means the code will be more reliable as the clients attribute can only be changed by the methods in this class
    def __init__(self, encryptionEnabled, saveMessages):
        self.encryptionEnabled = encryptionEnabled
        self.saveMessages = saveMessages
        self.__clients = {}
        #Create a people file object
        self.peopleFile = person.File("people.json", "server")
        #If this is the first time the server has been run then perform first time setup
        if self.peopleFile.newFile:
            print("First time setup")
            #Create the people array inside the people file
            self.peopleFile.createObject("people", [])
        #Load the people array from the people file
        self.loadPeople()
    def addClient(self,client):
        print("New client added")
        print("UserID:",client.userID)
        self.__clients[client.userID] = client
    def removeClient(self,client):
        print(client.userID,"disconnected")
        self.__clients.pop(client.userID)
    def sendMessage(self,sendData,userID):
        print(self.__clients)
        #Checks if client exists in the dictionary, if it does then send the message
        #If not then print error message
        client = self.__clients.get(userID, None)  # Get the client or None if not found
        if client:
            client.sendMessage(sendData)
        else:
            print(f"User with userID {userID} not found.")
    def clientConnected(self,userID):
        #This method will return true if the client is connected
        client = self.__clients.get(userID, None)
        if client:
            return True
        else:
            return False
    def outputClients(self):
        print(self.__clients)
    def updateUserID(self,oldUserID,newUserID):
        #This method will update the userID of a client and change the dictionary key
        print("Updating user ID")
        #Get the client object to change the key for 
        client = self.__clients.get(oldUserID, None)
        #If the client exists then change the key
        if client:
            #Change the attribute
            client.userID = newUserID
            #Change the key in the dictionary
            self.__clients[newUserID] = client
            #Remove the old key
            del self.__clients[oldUserID]
        else:
            print("User with userID"+ str(oldUserID) +"not found.")
    def getPublicKey(self,userID):
        try:
            print(self.people)
            return self.people[str(userID)].getPublicKey()
        except:
            print("User with userID",userID,"not found.")
            return None
    def loadPeople(self):
        #load list of people
        peopleArray = self.peopleFile.readObject("people")
        self.people = {}
        #Create a person object for each person in the people array
        for eachPerson in peopleArray:
            newPersonFile = person.Person(eachPerson, "server")
            self.people[eachPerson] = newPersonFile
    def addPerson(self, userID, username):
        #check if person already exists
        if userID in self.people:
            print("Person already exists")
            return
        #Add a person to the people list
        newPersonFile = person.Person(userID, "server" ,username)
        self.people[userID] = newPersonFile
        self.peopleFile.appendObject("people",userID)
    def saveMessage(self,senderID,messageContent):
        #This method will save a message to the sender's file
        self.people[senderID].appendChat(False, messageContent)
    def addToBuffer(self,recipientID,messageContent):
        #This method will add a message to the buffer
        self.people[recipientID].appendBuffer(messageContent)
    def getBuffers(self,userID):
        #This method will return the buffer of a user
        return self.people[userID].getBuffers()
    def clearBuffer(self,userID):
        #This method will clear the buffer of a user
        self.people[userID].clearBuffer()
        

class Client:
    def __init__(self,socket,host,userID,clientsQueue):
        #Setting attributes
        self.socket = socket
        self.host = host
        #username is not known when the client first connects, this will be set when the client sends a request to create a new user
        self.username = ""
        self.userID = userID
        #clientsQueue is a queue object that will be used to store the clients dictionary
        self.clientsQueue = clientsQueue
        self.active = True
    def recieveMessage(self):
        #Will run in seperate thread
        buffer = "" 
        while self.active:
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
                    receivedRequest= data.receivedData(singleRequest)
                    self.handleRequest(receivedRequest)
                except json.JSONDecodeError as e:
                    #Print out any other JSON decode errors
                    print("JSON Decode Error:", e)
    def sendMessage(self,sendData):
        #This method will send a completed JSON request to the server
        self.socket.send(sendData.encode())
    def handleRequest(self,receivedRequest):
        if self.active:
            print("Handling request")
            #Main handler method for when data is received from the client
            #This will be added to later as more request types are added
            requestType = receivedRequest.get("requestType")
            print("Request type:",requestType)
            if requestType == 0:
                self.handleNewUser(receivedRequest)
            if requestType == 2:
                self.handleGetPublicKey(receivedRequest)
            if requestType == 4:
                self.handleMessage(receivedRequest)
            if requestType == 5:
                self.handleSetUserID(receivedRequest)
            if requestType == 6:
                self.handleSetPublicKey(receivedRequest)
            if requestType == 7:
                self.disconnect()
    def disconnect(self):
        #If the request type is 7 then the client has disconnected
        print("Client disconnected:", self.userID)
        allClients = self.clientsQueue.get()
        allClients.removeClient(self)
        self.clientsQueue.put(allClients)
        #Set the active attribute to false so the recieveMessage method will stop
        self.active = False
        #Close the socket
        self.socket.close()
    def handleNewUser(self,receivedRequest):
        #Sets username attribute to received data and prints out information about the new user
        self.username = receivedRequest.get("username")
        print("New User Connected!")
        print("Host:",self.host)
        print("UserID:",self.userID)
        print("Username:",self.username)
        self.newUserResponse()
        
    def newUserResponse(self):
        #This method will send a response to the client with their userID generated by the server
        userIDResponse = data.SendData()
        userIDResponse.append("requestType",8)
        userIDResponse.append("userID",self.userID)
        self.sendMessage(userIDResponse.createJSON())
    
    def continueResponse(self):
        #This method will send a response to the client to continue
        continueResponse = data.SendData()
        continueResponse.append("requestType",8)
        self.sendMessage(continueResponse.createJSON())

    def handleMessage(self,receivedRequest):
        print("Handling message")
        #This method will forward a message to the recipient
        #This means if required this data can be stored later
        allClients = self.clientsQueue.get()
        forwardRequest = data.SendData()
        #Check if recipient is connected
        #If not then place the message in the buffer
        allClients.outputClients()
        if not allClients.clientConnected(int(receivedRequest.get("recipientID"))):
            #Debug print statements
            print("User with userID",receivedRequest.get("recipientID"),"not found.")
            print("Placing in buffer")
            print("People",allClients.people)
            #Add person if they do not already exist
            #If they do then the addPerson method will do nothing and print a message
            allClients.addPerson(receivedRequest.get("recipientID"), receivedRequest.get("recipientID"))
            #Add the entire request to the recipient buffer
            allClients.addToBuffer(receivedRequest.get("recipientID"),receivedRequest)
            print("Buffer:",allClients.getBuffers(receivedRequest.get("recipientID")))
            self.clientsQueue.put(allClients)
            return
        forwardRequest.append("requestType",4)
        forwardRequest.append("recipientID",receivedRequest.get("recipientID"))
        forwardRequest.append("senderID",receivedRequest.get("senderID"))
        forwardRequest.append("messageContent",receivedRequest.get("messageContent"))
        forwardRequest.append("username",receivedRequest.get("username"))
        if allClients.encryptionEnabled == True:
            print("Encryption enabled")
            #Add the signature to the message if encryption is enabled
            forwardRequest.append("signature",receivedRequest.get("signature"))
            #Add the sender's public key from server storage to the message
            forwardRequest.append("senderPublicKey",allClients.getPublicKey(int(receivedRequest.get("senderID"))))
        #If encryption is not enabled and saveMessages is true then save the message
        if allClients.saveMessages == True:
            print("Saving message")
            #Add a new person, if they already exists the 
            #addPerson method will do nothing and print a message
            allClients.addPerson(receivedRequest.get("recipientID"), receivedRequest.get("recipientID"))
            allClients.saveMessage(receivedRequest.get("recipientID"),receivedRequest.get("messageContent"))
        print("New message to forward to ",receivedRequest.get("recipientID"))
        allClients.sendMessage(forwardRequest.createJSON(),int(receivedRequest.get("recipientID")))
        self.clientsQueue.put(allClients)
    def handleSetUserID(self,receivedRequest):
        #This method will set the userID attribute to the received userID
        print("Updating user ID from",self.userID,"to",receivedRequest.get("userID"))
        self.newUserID = receivedRequest.get("userID")
        allClients = self.clientsQueue.get()
        print("Allclients update userID")
        allClients.outputClients()
        print("Whole queue",self.clientsQueue)
        allClients.updateUserID(self.userID,self.newUserID)
        allClients.addPerson(str(self.userID), str(self.userID))
        buffer = allClients.getBuffers(str(self.userID))
        self.clientsQueue.put(allClients)
        #Wait for client to launch the GUI
        time.sleep(0.5)
        self.sendBuffer(buffer,allClients)
    def sendBuffer(self, buffer, allClients):
        #This method will send the buffer to the client
        #Iterate through each request stored in the buffer
        for item in buffer.items():
            time.sleep(0.1)
            #Print out the request for debugging
            print("Item:",item[1])
            #Send the request to the client
            self.handleMessage(item[1])
        allClients.clearBuffer(str(self.userID))

    def handleSetPublicKey(self,receivedRequest):
        self.publicKey = receivedRequest.get("publicKey").encode('utf-8')
        allClients = self.clientsQueue.get()
        #Get the current public key of the user
        #By default this set to None
        self.currentPublicKey = allClients.getPublicKey(self.userID)
        print("Current public key:",self.currentPublicKey)
        print(type(self.currentPublicKey))
        print("Encryption enabled:",allClients.encryptionEnabled)
        print(type(allClients.encryptionEnabled))
        #Only set the public key and store in the file if encryption is enabled
        #And the public key is currently set to None
        if self.currentPublicKey == None and allClients.encryptionEnabled:
            print("Setting public key read only")
            allClients.people[str(self.userID)].setPublicKey(self.publicKey.decode('utf-8'))
        #print("Public key set to",self.publicKey)
        self.clientsQueue.put(allClients)
    def handleGetPublicKey(self,receivedRequest):
        try:
            print(receivedRequest.getDict())
            #This method will send the public key of the requested user to the client
            userIDToGet = receivedRequest.get("userID")
            allClients = self.clientsQueue.get()
            publicKey = allClients.getPublicKey(int(userIDToGet))
            #Make new response object and send the public key
            print("Public key to send:",publicKey)
            publicKeyResponse = data.SendData()
            publicKeyResponse.append("requestType",3)
            publicKeyResponse.append("userID",userIDToGet)
            publicKeyResponse.append("publicKey",publicKey)
            self.sendMessage(publicKeyResponse.createJSON())
        except AttributeError:
            print("User with userID",userIDToGet,"not found.")
            publicKeyResponse = data.SendData()
            publicKeyResponse.append("requestType",3)
            publicKeyResponse.append("userID",userIDToGet)
            publicKeyResponse.append("publicKey","None")
            self.sendMessage(publicKeyResponse.createJSON())
            #Close the queue so it can be used again
            return
        #Close the queue so it can be used again
        self.clientsQueue.put(allClients)
        