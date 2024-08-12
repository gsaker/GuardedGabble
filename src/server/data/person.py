import datetime
from data.file import File
from pathlib import Path
import os 
class Person(File):
    def __init__(self, userID, programName, username=None):
        # Initialize Person object with userID and username
        self.programName = programName
        self.userID = userID
        self.username = username
        self.filepath = Path("people/" + self.userID + ".json")
        self.chatID = 0
        self.bufferID = 0
        self.fullPath = super().getFullPath(self.filepath)
        existed = os.path.isfile(self.fullPath)
        self.publicKey = None
        super().__init__(self.filepath, self.programName)
        # If the file does not exist, set initial attributes
        if not existed:
            print("Setting attributes")
            super().createObject("username", self.username)
            super().createObject("userID", self.userID)
            super().createObject("publicKey", None)
            super().createObject("chatID", 0)
            super().createObject("bufferID", 0)
            super().createObject("chats", {})
            super().createObject("buffer",{})
        else:
            self.username = super().readObject("username")
    def appendChat(self, receivedBool, messageContent):
        # Append a new chat to the Person object
        self.chatID = super().readObject("chatID")
        date = datetime.datetime.now()
        # Create chat object with date, received status, and message content
        chat = {
            "date": str(date.isoformat()),
            "received": receivedBool,
            "message": messageContent
        }
        # Read chats dictionary from JSON
        chats = super().readObject("chats")
        # Append chat to dictionary at the next chatID
        chats[self.chatID] = chat
        # Write updated chats back to JSON
        super().createObject("chats", chats)
        # Increment chatID
        self.chatID += 1
        super().createObject("chatID", self.chatID)
    def appendBuffer(self, recievedRequest):
        # Get the current bufferID and buffer from the Person object
        self.bufferID = super().readObject("bufferID")
        buffer = super().readObject("buffer")
        # Get the dictionary from the recieved request
        # Since we can't store the request object we get the ditionary instead
        recievedDict = recievedRequest.getDict()
        print(recievedDict)
        # Add the dictionary to the buffer
        buffer[self.bufferID] = recievedDict
        # Write the updated buffer back to the JSON
        super().createObject("buffer", buffer)
        # Increment the bufferID
        self.bufferID += 1
        # Store the increment bufferID back to the JSON
        super().createObject("bufferID", self.bufferID)
    def clearBuffer(self):
        # Clear the buffer by setting it to an empty dictionary
        super().createObject("buffer", {})
        # Reset the bufferID to 0
        super().createObject("bufferID", 0)
    def getBuffers(self):
        # Retrieve the buffer from the Person object
        return super().readObject("buffer")
    def getChat(self, chatID):
        # Retrieve a specific chat from the Person object
        return super().readObject(["chats"][int(chatID)])
    def getChats(self):
        return super().readObject("chats")
    def getPublicKey(self):
        return super().readObject("publicKey")
    def setPublicKey(self, publicKey):
        super().createObject("publicKey", publicKey)
    def readJSON(self):
        return super().readJSON()