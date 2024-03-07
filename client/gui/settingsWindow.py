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
        self.app.configFile.createObject("server", self.serverAddressTextbox.text())
        self.app.configFile.createObject("port", self.serverPortTextbox.text())
        self.app.configFile.createObject("username", self.usernameTextbox.text())
        #Restart application
        self.app.stop()
