import datetime
from file import File
from pathlib import Path
class Person(File):
    def __init__(self, userID, username):
        self.userID = userID
        self.username = username
        self.filepath = Path("people/" + self.userID + ".json")
        self.chatID = 0
        super().__init__(self.filepath)
    def appendChat(self, recievedBool, messageContent):
        date = datetime.datetime.now()
        #Create chat object
        chat = {
            "date": date,
            "recieved": recievedBool,
            "message": messageContent
        }
        #Append chat object to chats list
        super.createObject(self.chatID, chat)
        #Increment chatID
        self.chatID += 1
    def getChat(self, chatID):
        return super.readObject(chatID)
