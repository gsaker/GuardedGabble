import json
import os
from pathlib import Path

class File:
    def __init__(self, filepath, programName):
        self.programName = programName
        #Filepath is relative to the base data directory
        self.newFile = False
        self.filePath = filepath
        self.dataDir = self.loadDataDir()
        self.fullPath = os.path.join(self.dataDir, self.filePath)
        self.createDirectory(os.path.dirname(self.fullPath))
        #Create file if it doesn't exist
        if not os.path.isfile(self.fullPath):
            print("File not found, creating file")
            self.newFile = True
            writeFile = open(self.fullPath, "w")
            json.dump({}, writeFile)
            writeFile.close()
    def getFullPath(self,filepath):
        #Get full path of file, sets to string in case it's a Path object
        filePath = str(filepath)
        dataDir = str(self.loadDataDir())
        fullPath = os.path.join(dataDir, filePath)
        return fullPath
    def loadDataDir(self):
        #Create data directory if it doesn't exist
        dataDir = os.path.join(os.path.expanduser("~"), ".config", self.programName)
        if not os.path.isdir(dataDir):
            os.makedirs(dataDir)
        #Return data directory
        return os.path.join(os.path.expanduser("~"), ".config", self.programName)
    def createDirectory(self, directoryPath):
        #Create directory if it doesn't exist
        if not os.path.isdir(directoryPath):
            os.makedirs(directoryPath)
    def createObject(self,key,data):
        jsonData = self.readJSON()
        # create newData tuple
        newData = {key: data}
        # update either adds or modifies the data
        jsonData.update(newData)
        self.writeJSON(jsonData)
    def appendObject(self,key,data):
        jsonData = self.readJSON()
        # append data to existing key
        jsonData[key].append(data)
        self.writeJSON(jsonData)
    def removeObject(self,key, data):
        jsonData = self.readJSON()
        # remove data from existing key
        jsonData[key].remove(data)
        self.writeJSON(jsonData)
    def readObject(self,key):
        jsonData = self.readJSON()
        return jsonData[key]
    def readJSON(self):
        #Read JSON file and return as dictionary
        with open(self.fullPath, "r") as file:
            return json.load(file)
    def writeJSON(self, jsonData):
        #Write dictionary to JSON file
        with open(self.fullPath, "w") as file:
            json.dump(jsonData, file)
            
