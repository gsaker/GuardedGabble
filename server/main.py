import socket
import threading
from net import *
import random
from queue import Queue
class Server:
    def __init__(self):
        print("Starting Server")
        # Set the host and port for the server to listen on
        localhost = '192.168.40.12287liwequasjb vkehflhefwhjewafjl'
        port = 64147

        # Start a new thread to accept incoming client connections
        acceptClients = threading.Thread(target=self.startServer,args=(localhost,port))
        acceptClients.start()
        print("Server started succesfully")
        # Create an instance of the Clients class to store all connected clients
        self.allClients = client.Clients()

    def startServer(self,host,port):
        """
        This function starts the server and listens for incoming client connections.
        For each client that connects, a new client object is created and added to the allClients dictionary.
        """
        serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serverSocket.bind((host,port))
        serverSocket.listen(5)
        # Create a queue for each client to store incoming messages
        while True:
            clientsQueue = Queue()
            clientSocket, clientAddress= serverSocket.accept()

            # Generate a random userID for each client (temporary, will be replaced with a database)
            userID = random.randint(100000,999999)

            # Create a new client object and add it to the allClients dictionary
            newClient = client.Client(clientSocket,clientAddress,userID,clientsQueue)
            self.allClients.addClient(newClient)
            clientsQueue.put(self.allClients)

            # Start a new thread to receive messages from the client
            receiveThread = threading.Thread(target=newClient.recieveMessage)
            receiveThread.start()
if __name__ == "__main__":
    Server()
    print("Done")

