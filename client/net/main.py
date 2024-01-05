import threading
from net import server
from time import sleep
#Test data
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
        #Small delay for server to process request
        sleep(0.5)
        #send message loop
        while True:
            recipientID = input("Enter recipient ID: ")
            messageToSend = input("Enter message to send: ")
            mainServer.messageRequest(messageToSend,recipientID)
connectServer()
print("Done")