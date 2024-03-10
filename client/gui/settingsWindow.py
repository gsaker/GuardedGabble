from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
#Use a QDialog to create a new window
class SettingsWindow(QDialog):
    def __init__(self,app):
        #Pass the app object to the window 
        #this is so we can save the settings to the config file and restart the application
        self.app = app
        super().__init__()
        #Set the theme to dark
        darkStylesheet = qdarkstyle.load_stylesheet_pyqt5()
        self.setStyleSheet(darkStylesheet)
        #Set the title and size of the window
        self.setWindowTitle("Settings")
        self.setGeometry(100, 100, 300, 200)
        #Create widgets 
        #Server address
        self.serverAddressLabel = QLabel("Server Address")
        self.serverAddressTextbox = QLineEdit(str(self.app.serverHost))
        self.serverAddressLayout = QHBoxLayout()
        self.serverAddressLayout.addWidget(self.serverAddressLabel)
        self.serverAddressLayout.addWidget(self.serverAddressTextbox)
        self.serverAddressWidget = QWidget()
        self.serverAddressWidget.setLayout(self.serverAddressLayout)
        #Server port
        self.serverPortLabel = QLabel("Server Port")
        self.serverPortTextbox = QLineEdit(str(self.app.serverPort))
        self.serverPortLayout = QHBoxLayout()
        self.serverPortLayout.addWidget(self.serverPortLabel)
        self.serverPortLayout.addWidget(self.serverPortTextbox)
        self.serverPortWidget = QWidget()
        self.serverPortWidget.setLayout(self.serverPortLayout)
        #Username
        self.usernameLabel = QLabel("Username")
        self.usernameTextbox = QLineEdit(str(self.app.username))
        self.usernameLayout = QHBoxLayout()
        self.usernameLayout.addWidget(self.usernameLabel)
        self.usernameLayout.addWidget(self.usernameTextbox)
        self.usernameWidget = QWidget()
        self.usernameWidget.setLayout(self.usernameLayout)
        #Save button
        self.saveButton = QPushButton("Save")
        self.saveButton.clicked.connect(self.saveSettings)
        #Add widgets to main layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.serverAddressWidget)
        self.layout.addWidget(self.serverPortWidget)
        self.layout.addWidget(self.usernameWidget)
        self.layout.addWidget(self.saveButton)
        self.setLayout(self.layout)
    def saveSettings(self):
        #Save settings to config file
        if self.validateUsername(self.usernameTextbox.text()):
            self.app.configFile.createObject("username", self.usernameTextbox.text())
            if self.validateServer(self.serverAddressTextbox.text()):
                self.app.configFile.createObject("server", self.serverAddressTextbox.text())
                if self.validatePort(self.serverPortTextbox.text()):
                    self.app.configFile.createObject("port", self.serverPortTextbox.text())
                    #Restart application
                    self.app.stop()
    def validateUsername(self, username):
        #Check if username is valid
        if len(username) > 3 and len(username) < 20:
            pass
        else:
            #Show a dialog box if the username is invalid
            self.app.showError("Username must be more than 3 and less than 20 characters")
            return False
        if username.isalnum():
            return True
        else:
            self.app.showError("Username can only contain letters and numbers")
            return False
    def validateServer(self, server):
        #Check if server address is valid
        #If it contains a . then it's valid
        if "." in server:
            return True
        else:
            self.app.showError("Server address is invalid, should be of the form x.x.x.x or a domain name")
            return False
    def validatePort(self, port):
        #Check if port is valid
        try:
            port = int(port)
            if port > 0 and port <= 65535:
                return True
            else:
                self.app.showError("Port must be between 0 and 65535")
                return False
        except:
            self.app.showError("Port must be a number")
            return False

