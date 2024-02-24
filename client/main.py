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
    def __init__(self, appNo):
        print("Starting GuardedBabble")
        #This is just test data, in the future there will be a method that runs first time setup
        self.serverHost = '127.0.0.1'
        self.serverPort = 64147
        self.username = "User1"
        self.appNo = appNo
        #Create config and people file object
        self.configFile = file.File("config.json", self.appNo)
        self.peopleFile = file.File("people.json", self.appNo)
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
            #Send the stored userID to the server if it exists in the config file
            self.mainServer.setUserIDRequest(self.configFile.readObject("userID"))
        #Set stored userID
        self.userID = self.configFile.readObject("userID")
        self.mainServer.userID = self.userID
        #Load people
        self.loadPeople()
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
            newPersonFile = person.Person(eachPerson, appNo)
            self.people[eachPerson] = newPersonFile
    def addPerson(self, userID, username):
        #check if person already exists
        if userID in self.people:
            print("Person already exists")
            return
        #Add a person to the people list
        newPersonFile = person.Person(userID, appNo ,username)
        self.people[userID] = newPersonFile
        self.peopleFile.appendObject("people",userID)
    def recievedMessage(self, senderID, messageContent):
        #Print the message (for debugging purposes)
        print("Recieved message from",senderID)
        print("Message:",messageContent)
        print(self.people)
        #If the sender is not in the people list then add them
        if senderID not in self.people:
            print("Adding new person to people list")
            self.addPerson(str(senderID), str(senderID))
            #Emit signal to add person to GUI
            self.chatWindow.addPersonToGUI.emit()
        #Add the message to the person's chat history
        self.people[str(senderID)].appendChat(True, messageContent)
        #Emit signal to update chat window in different thread
        self.chatWindow.messageReceived.emit()
if __name__ == "__main__":
    #Displays an error message if the user does not enter an app number
    if len(sys.argv) != 2:
        print("Usage: python main.py <appNo>")
        sys.exit(1)
    #Set the appnumber variable
    appNo = sys.argv[1]
    mainProcess = App(appNo)