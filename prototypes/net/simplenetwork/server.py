import socket 
def startServer(host,port):
    serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #Double bracket used to make tuple
    serverSocket.bind((host,port))
    #This lines sets the listen backlog queue lenth for 5. 
    #This means up to 5 clients can be waiting in the queue at a time
    serverSocket.listen(5)
    #This sets creates a new socket object clientScoekt and creates a tupple clientAddress with IP and port
    clientSocket, clientAddress= serverSocket.accept()
    #Loop to keep recieving/sending messages
    while True:
        #Up to 1024 bytes can be recieved
        #recievedMessage = clientSocket.recv(1024)
        #recievedMessage = recievedMessage.decode()
        #print("Client:", recievedMessage)
        sendMessage = input("Server:")
        clientSocket.send(sendMessage.encode())
    clientSocket.close()
#In this example we will use the localhost as the server and client
#Are running on the same machine
startServer('127.0.0.1',64148)