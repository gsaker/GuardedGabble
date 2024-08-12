from data import file
from data import person
from net import server
import threading
from time import sleep
from gui import chatWindow
from net import encrypt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMessageBox
import sys
import os
import random
#Test data
class App:
    def __init__(self, appNo):
        print("Starting GuardedBabble")
        #This is just test data, in the future there will be a method that runs first time setup
        self.serverHost = '127.0.0.1'
        self.serverPort = 64147
        self.username = "User1"
        self.appNo = appNo
        self.encryptionEnabled = True
        #Create config and people file object
        self.configFile = file.File("config.json", self.appNo)
        self.peopleFile = file.File("people.json", self.appNo)
        if self.configFile.newFile:
            #Connect to server before creating config file
            self.connectServer()
            print("First time setup")
            print("Creating config file")
            #At this point as this is the first time opening the app, we need to run the first time setup
            #I will implement this later, for now the test data is above
            self.configFile.createObject("server", self.serverHost)
            self.configFile.createObject("port", self.serverPort)
            self.configFile.createObject("username", self.username)
            userID = random.randint(100000,999999)
            #Still set the userID request to the server
            self.mainServer.setUserIDRequest(userID)         
            #Small delay for server to process request, this is terrible and will be replaced
            sleep(0.5)
            self.configFile.createObject("userID", self.mainServer.userID)
            self.peopleFile.createObject("people", [])
            if self.encryptionEnabled:
                #Generate keys and store them in the config file
                self.privateKey, self.publicKey = encrypt.generateKeys()
                #Need to convert to string to store in JSON
                self.configFile.createObject("privateKey", self.privateKey.decode('utf-8'))
                self.configFile.createObject("publicKey", self.publicKey.decode('utf-8'))
        else:
            #If config file exists then load data from it
            print("Loading config file")
            self.serverHost = self.configFile.readObject("server")
            self.serverPort = int(self.configFile.readObject("port"))
            print("Server:",self.serverHost)
            print("Port:",self.serverPort)
            #Connect to server after server host and port are loaded
            self.connectServer()
            self.username = self.configFile.readObject("username")
            #Send the stored userID to the server if it exists in the config file
            self.waitForContinue()


            

            self.mainServer.setUserIDRequest(self.configFile.readObject("userID"))
            #Load keys from config file
            #Need to convert to bytes to use in encryption
            if self.encryptionEnabled:
                self.privateKey = self.configFile.readObject("privateKey").encode('utf-8')
                self.publicKey = self.configFile.readObject("publicKey").encode('utf-8')
        #Set stored userID
        self.userID = self.configFile.readObject("userID")
        self.mainServer.userID = self.userID
        #Load people
        self.loadPeople()
        if self.encryptionEnabled:
            #Send public key to server
            self.mainServer.setPublicKeyRequest(self.publicKey)
        #sleep(2)
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
    def removePerson(self, userID):
        #Remove a person from the people list
        self.peopleFile.removeObject("people",userID)
        del self.people[userID]
        self.chatWindow.addPersonToGUI.emit()
        self.chatWindow.personRemoved.emit()
    def receivedMessage(self, senderID, messageContent):
        #Print the message (for debugging purposes)
        print("received message from",senderID)
        print("Message:",messageContent)
        print(self.people)
        self.chatWindow.addPersonToGUI.emit()
        #Add the message to the person's chat history
        self.people[str(senderID)].appendChat(True, messageContent)
        #Emit signal to update chat window in different thread
        #Send the message with the signal 
        self.chatWindow.messageReceived.emit(senderID)
        #self.chatWindow.messageReceived.emit()
    def recievedPublicKey(self,userID,publicKey):
        #Add the public key to the person's file
        self.people[str(userID)].publicKey = publicKey
    def stop(self):
        #Disconnect 
        self.mainServer.disconnect()
        #Stop the application
        os._exit(0)
    def showError(self,message):
        # Simple method to show an error message
        app = None
        if not QApplication.instance():
            app = QApplication(sys.argv)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle("Error")
        msg.exec_()
        if app:
            app.exit()  # Only exit the QApplication if we created it
    def waitForContinue(self):
        self.continueResponseReceived = False
        counter = 0
        #Wait until self.continueResponseReceived is true, timeout after 5 seconds
        while not self.continueResponseReceived:
            sleep(0.1)
            counter += 1
            if counter == 50:
                self.showError("Server connection failed")
                self.stop()
                break

if __name__ == "__main__":
    #Displays an error message if the user does not enter an app number
    if len(sys.argv) != 2:
        print("Usage: python main.py <appNo>")
        #Set the appnumber variable
        appNo = "GuardedBabble"
    else:
        appNo = sys.argv[1]
    mainProcess = App(appNo)