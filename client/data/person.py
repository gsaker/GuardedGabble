import datetime
from data.file import File
from pathlib import Path
import os 
class Person(File):
    def __init__(self, userID, programName, username=None ):
        # Initialize Person object with userID and username
        self.programName = programName
        self.userID = userID
        self.username = username
        self.filepath = Path("people/" + self.userID + ".json")
        self.chatID = 0
        self.publicKey = None
        self.fullPath = super().getFullPath(self.filepath)
        existed = os.path.isfile(self.fullPath)
        super().__init__(self.filepath, self.programName)
        # If the file does not exist, set initial attributes
        if not existed:
            print("Setting attributes")
            super().createObject("username", self.username)
            super().createObject("userID", self.userID)
            super().createObject("chatID", 0)
            super().createObject("chats", {})
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
    def getChat(self, chatID):
        # Retrieve a specific chat from the Person object
        return super().readObject(["chats"][int(chatID)])
    def getChats(self):
        try:
            return super().readObject("chats")
        except:
            # If there is an error, then a chat is likely being written to the file at the same time
            return {}
    def readJSON(self):
        return super().readJSON()
    def setUsername(self, username):
        # Set the username of the Person object
        self.username = username
        super().createObject("username", self.username)