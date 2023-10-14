import json
#This is the class that crafts requests sent to the server
class Request:
    def __init__(self):
        self.__requestDict = {}
    #This method appends a key and value to the request dictionary
    def append(self, key, value):
        self.__requestDict[key] = value
    #Once the request is complete, this method will return the JSON string ready to be sent to the server
    def createJSON(self):
        return json.dumps(self.__requestDict)

#This is the class that handles responses recieved from the server
class Response:
    def __init__(self, responseString):
        #json.loads() converts a JSON string into a dictionary
        self.__responseDict = json.loads(responseString)
    def get(self, key):
        return self.__responseDict[key]
#This is sample data that would be either loaded from other objects or user input
recipientID = 2
senderID = 1
def sendMessage(messageContent):
    message = Request()
    message.append("requestType",4)
    message.append("recipientID",recipientID)
    message.append("senderID",senderID)
    message.append("messageContent",messageContent)
    requestJSON = message.createJSON()
    print(requestJSON)
    #This is where the request would be sent to the server
    #The server would then send a response back
    #In this case we will use the same request
    response = Response(requestJSON)
    print(response.get("requestType"))
    print(response.get("recipientID"))
    print(response.get("senderID"))
    print(response.get("messageContent"))
sendMessage("Hello World!")