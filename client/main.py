from data import file
from data import person
from net import server
import threading
from time import sleep
from gui import chatWindow
from PyQt5.QtWidgets import QApplication
import sys
#Test data
class App:
    def __init__(self):
        print("Starting GuardedBabble")
        #This is just test data, in the future there will be a method that runs first time setup
        self.serverHost = '127.0.0.1'
        self.serverPort = 64147
        self.username = "User1"
        #Create config and people file object
        self.configFile = file.File("config.json")
        self.peopleFile = file.File("people.json")
        #Connect to server
        self.connectServer()
        if self.configFile.newFile:
            print("First time setup")
            print("Creating config file")
            #At this point as this is the first time opening the app, we need to run the first time setup
            #I will implement this later, for now the test data is above
            self.configFile.createObject("server", self.serverHost)
            self.configFile.createObject("port", self.serverPort)
            self.configFile.createObject("username", self.username)
            self.mainServer.newUserRequest(self.username)
            #Small delay for server to process request, this is terrible and will be replaced
            sleep(0.5)
            self.configFile.createObject("userID", self.mainServer.userID)
            self.peopleFile.createObject("people", [])
        else:
            #If config file exists then load data from it
            print("Loading config file")
            self.serverHost = self.configFile.readObject("server")
            self.serverPort = self.configFile.readObject("port")
            self.username = self.configFile.readObject("username")
        #Set stored userID
        self.userID = self.configFile.readObject("userID")
        #Load people
        self.loadPeople()
        #Add test people to check functionality
        self.addPerson("1","User1")
        self.addPerson("2","User2")
        self.addPerson("3","User3")
        self.addPerson("4","User4")
        self.addPerson("5","User5")
        self.addPerson("6","User6")
        self.addPerson("7","User7")
        self.addPerson("8","User8")
        self.addPerson("9","User9")
        self.addPerson("10","User10")
        self.addPerson("11","User11")
        self.addPerson("12","User12")
        self.addPerson("13","User13")
        self.addPerson("14","User14")
        self.addPerson("15","User15")
        self.addPerson("16","User16")
        self.addPerson("17","User17")
        self.addPerson("18","User18")
        self.addPerson("19","User19")
        self.addPerson("20","User20")
        #Create chat window object
        self.applicationWindow = QApplication(sys.argv)
        self.chatWindow = chatWindow.MainWindow(self)
        self.chatWindow.show()
        #Exit when window is closed
        sys.exit(self.applicationWindow.exec_())
    def connectServer(self):
        #Creating server object
        self.mainServer=server.Server(self.serverHost,self.serverPort, self)
        #Create a config file object to get username
        #If connection is successful then start recieve thread and start recieving messages
        if self.mainServer.connectServer():
            receiveThread = threading.Thread(target=self.mainServer.recieveMessage)
            receiveThread.start()
    def loadPeople(self):
        #load list of people
        peopleArray = self.peopleFile.readObject("people")
        self.people = {}
        for eachPerson in peopleArray:
            newPersonFile = person.Person(eachPerson)
            self.people[eachPerson] = newPersonFile
    def addPerson(self, userID, username):
        #check if person already exists
        if userID in self.people:
            print("Person already exists")
            return
        #Add a person to the people list
        newPersonFile = person.Person(userID, username=username)
        self.people[userID] = newPersonFile
        self.peopleFile.appendObject("people",userID)
    def recievedMessage(self, senderID, messageContent):
        #This method will be called when a message is recieved
        #This will be added to later as more request types are added
        #For now it will just print the message
        print("Recieved message from",senderID)
        print("Message:",messageContent)
        self.people[senderID].addMessage(messageContent)
        self.chatWindow.updateChatWindow()
if __name__ == "__main__":
    mainProcess = App()
    print("Done")