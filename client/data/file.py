import os
import json
programName = "GuardedBabble"
class File:
    def __init__(self, filepath):
        self.filePath = filepath
        self.dataDir = self.loadDataDir()
        self.fullPath = os.path.join(self.dataDir, self.filePath)
        try:
            with open(self.fullPath, "r") as file:
                pass
        except FileNotFoundError:
            writeFile = open(self.fullPath, "w")
            writeFile.close()
    def loadDataDir(self):
        if not os.path.isdir(self.dataDir):
            os.makedirs(self.dataDir)
        return os.path.join(os.path.expanduser("~"), ".config", programName)
    def createObject(self,key,data):
        fullPath = os.path.join(self.dataDir, self.filePath)
        newData = {key: data}
        with open(fullPath, "r") as file:
            jsonData = json.load(file)  # read existing JSON data
        jsonData.update(newData)  # add new data to existing JSON object
        with open(fullPath, "w") as file:
            json.dump(jsonData, file)  # write updated JSON object to file
testFile = File("test.json")
