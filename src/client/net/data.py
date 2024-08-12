import json
class SendData:
    def __init__(self):
        self.__requestDict = {}
    #This method appends a key and value to the request dictionary
    def append(self, key, value):
        self.__requestDict[key] = value
    #Once the request is complete, this method will return the JSON string ready to be sent to the server
    def createJSON(self):
        return json.dumps(self.__requestDict)
class receivedData:
    def __init__(self, responseString):
        #json.loads() converts a JSON string into a dictionary
        print("Received data:",responseString)
        self.__responseDict = json.loads(responseString)
    def get(self, key):
        return self.__responseDict[key]