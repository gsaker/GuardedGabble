from . import data
from data import person
import sys
sys.path.append(".")
encryptionEnabled = True
saveMessages = True
class Clients:
    #This class will hold all the clients connected to the server
    #Clients can only be added or removed from this class due to the attribute being private
    #This means the code will be more reliable as the clients attribute can only be changed by the methods in this class
    def __init__(self):
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
        self.__clients.pop(client.host)
    def sendMessage(self,sendData,userID):
        print(self.__clients)
        #Checks if client exists in the dictionary, if it does then send the message
        #If not then print error message
        client = self.__clients.get(userID, None)  # Get the client or None if not found
        if client:
            client.sendMessage(sendData)
        else:
            print(f"User with userID {userID} not found.")
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
        #This method will return the public key of a client
        #Get the client object
        client = self.__clients.get(userID, None)
        #If the client exists then return the public key
        if client:
            return client.publicKey
        #Otherwise print an error message
        else:
            print("User with userID"+ str(userID) +"not found.")
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
    def recieveMessage(self):
        #Will run in seperate thread
        while True:
            #Keep trying to recieve data from the client
            receivedRequest = data.receivedData(self.socket.recv(2048))
            self.handleRequest(receivedRequest)
    def sendMessage(self,sendData):
        #This method will send a completed JSON request to the server
        self.socket.send(sendData.encode())
    def handleRequest(self,receivedRequest):
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
        userIDResponse.append("requestType",1)
        userIDResponse.append("userID",self.userID)
        self.sendMessage(userIDResponse.createJSON())
    def handleMessage(self,receivedRequest):
        print("Handling message")
        #This method will forward a message to the recipient
        #This means if required this data can be stored later
        allClients = self.clientsQueue.get()
        forwardRequest = data.SendData()
        forwardRequest.append("requestType",4)
        forwardRequest.append("recipientID",receivedRequest.get("recipientID"))
        forwardRequest.append("senderID",receivedRequest.get("senderID"))
        forwardRequest.append("messageContent",receivedRequest.get("messageContent"))
        if encryptionEnabled:
            #Add the signature to the message if encryption is enabled
            forwardRequest.append("signature",receivedRequest.get("signature"))
            forwardRequest.append("senderPublicKey",receivedRequest.get("senderPublicKey"))
        #If encryption is not enabled and saveMessages is true then save the message
        if not encryptionEnabled and saveMessages:
            print("Saving message")
            #Add a new person, if they already exists the 
            #addPerson method will do nothing and print a message
            allClients.addPerson(receivedRequest.get("senderID"), receivedRequest.get("senderID"))
            allClients.saveMessage(receivedRequest.get("senderID"),receivedRequest.get("messageContent"))
        print("New message to forward to ",receivedRequest.get("recipientID"))
        allClients.sendMessage(forwardRequest.createJSON(),int(receivedRequest.get("recipientID")))
        self.clientsQueue.put(allClients)

    def handleSetUserID(self,receivedRequest):
        #This method will set the userID attribute to the received userID
        print("Updating user ID from",self.userID,"to",receivedRequest.get("userID"))
        self.newUserID = receivedRequest.get("userID")
        allClients = self.clientsQueue.get()
        allClients.updateUserID(self.userID,self.newUserID)
        self.clientsQueue.put(allClients)
    def handleSetPublicKey(self,receivedRequest):
        #This method will set the public key attribute to the received public key
        #This is highly insecure and will be changed in the future
        self.publicKey = receivedRequest.get("publicKey").encode('utf-8')
        print("Public key set to",self.publicKey)
    def handleGetPublicKey(self,receivedRequest):
        try:
            print(receivedRequest)
            #This method will send the public key of the requested user to the client
            userIDToGet = receivedRequest.get("userID")
            allClients = self.clientsQueue.get()
            publicKey = allClients.getPublicKey(int(userIDToGet))
            #Make new response object and send the public key
            print("Public key to send:",publicKey)
            publicKeyResponse = data.SendData()
            publicKeyResponse.append("requestType",3)
            publicKeyResponse.append("userID",userIDToGet)
            publicKeyResponse.append("publicKey",publicKey.decode('utf-8'))
            self.sendMessage(publicKeyResponse.createJSON())
            #Close the queue so it can be used again
            self.clientsQueue.put(allClients)
        except AttributeError:
            print("User with userID",userIDToGet,"not found.")
            self.clientsQueue.put(allClients)
            return

