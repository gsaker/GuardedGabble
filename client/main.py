import threading
from net import server

serverHost = '127.0.0.1'
serverPort = 64147
username = "User1"
def connectServer():
    #Creating server object
    mainServer=server.Server(serverHost,serverPort)
    #If connection is successful then start recieve thread and start recieving messages
    if mainServer.connectServer():
        receiveThread = threading.Thread(target=mainServer.recieveMessage)
        receiveThread.start()
        mainServer.newUserRequest(username)
connectServer()
print("Done")