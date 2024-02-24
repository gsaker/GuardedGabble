import socket 
def startClient(host,port):
    #Create socket object
    clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #Double bracket used to make tuple
    clientSocket.connect((host,port))    
    #Loop to keep recieving/sending messages
    while True:
        sendMessage = input("Client:")
        clientSocket.send(sendMessage.encode())
        receivedMessage = clientSocket.recv(1024)
        print("Server:",receivedMessage.decode())
    clientSocket.close()
#In this example we will use the localhost as the server and client
#Are running on the same machine
startClient('127.0.0.1',64147)