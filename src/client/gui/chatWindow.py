import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from qdarkstyle import load_stylesheet_pyqt5
from PyQt5.QtWidgets import QInputDialog
from gui import helpWindow
from gui import settingsWindow
class MainWindow(QWidget):
    messageReceived = pyqtSignal(str)
    addPersonToGUI = pyqtSignal()
    personRemoved = pyqtSignal()
    def __init__(self, app):
        super().__init__()
        #set variable to acess passed through app object
        self.app = app
        self.initUI()

    def initUI(self):
        #loading the dark theme, in the future this will be a setting
        darkStylesheet = load_stylesheet_pyqt5()
        self.setStyleSheet(darkStylesheet)
        self.setWindowTitle('Chat Window' + str(self.app.appNo))
        #Set minimum width of window to make sure chat experience is consistent
        self.setGeometry(100, 100, 770, 700) 
        #QScrollarea to allow for scrollling through people list
        self.leftLayout = QVBoxLayout()
        self.chatSelectArea = QScrollArea()
        self.currentChatPerson = None
        #create buttons for each person in people list
        self.createPeopleButtons()

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        if self.currentChatPerson != None:
            self.openChatWindow(self.currentChatPerson)
        
        self.addUserButton = QPushButton('Add User')
        self.addUserButton.clicked.connect(self.addUserClicked)
        self.leftLayout.addWidget(self.addUserButton)
        self.leftLayout.addWidget(self.chatSelectArea)
        #create input box for chat messages
        self.messageInput = QTextEdit()
        self.messageInput.setPlaceholderText("Chat Message Here...")
        self.messageInput.setMaximumHeight(100)
        #connect enter key to send message
        self.messageInput.installEventFilter(self)

        #create buttons
        self.sendButton = QPushButton('Send')
        self.sendButton.clicked.connect(lambda _,: self.sendMessage())

        self.settingButton = QPushButton('Settings')
        #connect settings button to open settings window
        self.settingButton.clicked.connect(lambda _: self.openSettingsWindow())
        self.idButton = QPushButton(str(self.app.userID))
        self.quitButton = QPushButton('Quit')
        #connect quit button to stop the application
        self.quitButton.clicked.connect(lambda _: self.app.stop())
        self.helpButton = QPushButton('Help')
        #connect help button to open help window
        self.helpButton.clicked.connect(lambda _: self.openHelpWindow())


        #create layouts
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.sendButton)
        self.buttonLayout.addWidget(self.settingButton)
        self.buttonLayout.addWidget(self.idButton)
        self.buttonLayout.addWidget(self.quitButton)
        self.buttonLayout.addWidget(self.helpButton)


        self.inputLayout = QVBoxLayout()
        self.inputLayout.addWidget(self.messageInput)

        self.rightLayout = QVBoxLayout()
        self.rightLayout.addWidget(self.scrollArea)
        self.rightLayout.addLayout(self.inputLayout)

        self.topLayout = QHBoxLayout()
        self.topLayout.addLayout(self.leftLayout,1)
        self.topLayout.addLayout(self.rightLayout,3)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.buttonLayout)
        
        self.setLayout(self.mainLayout)
        self.messageReceived.connect(lambda senderID: self.openChatWindow(senderID=senderID))
        self.addPersonToGUI.connect(self.createPeopleButtons)
        self.personRemoved.connect(self.showNotExistError)
        self.newMessageDictionary = {}
    def addUserClicked(self):
        #Shows an input box to enter the userID and gets the outputs
        text, ok = QInputDialog.getText(self, 'Add User', 'Enter User ID:')
        # Only continue if the user clicked ok
        if ok:
            userId = text
            #Show error is userID contains non-numeric characters
            if not userId.isnumeric():
                self.app.showError("User ID must be a number")
                return
            # Add the user to the people list
            # For now we will user the userID as the username, when the other person sends a message the actual username will be populated
            self.app.addPerson(userId, userId)
            # Recreate the buttons to include the new user
            self.createPeopleButtons()
            #Get the public key from the server
            if self.app.encryptionEnabled:
                self.app.mainServer.getPublicKeyRequest(userId)
            self.openChatWindow(self.currentChatPerson)

    def createPeopleButtons(self):
        self.chatSelectArea.setWidgetResizable(True)
        # vbox layout so new buttons are added vertically
        self.chatSelectAreaLayout = QVBoxLayout()
        self.chatSelectAreaWidget = QWidget()
        self.chatSelectAreaWidget.setLayout(self.chatSelectAreaLayout)
        self.chatSelectArea.setWidget(self.chatSelectAreaWidget)
        self.buttonDictionary = {}
        for person in self.app.people:
            button = QPushButton(self.app.people[person].username)
            button.setStyleSheet("""
        QPushButton {
            background-color: #19232D;
            color: #ffffff;
            border: 2px solid #455364;
            border-radius: 10px;
            padding: 8px;
            font-size: 14px;
        }
        """)
            self.buttonDictionary[person] = button
            #call openChatWindow with the person object as an argument
            button.clicked.connect(lambda _, person=self.app.people[person]: self.openChatWindow(person))
            self.chatSelectAreaLayout.addWidget(button)
        #Iterate through people and set the selected button to the previously selected person
        if self.currentChatPerson != None:
            for person in self.app.people:
                if person == self.currentChatPerson.userID:
                    self.setSelectedButtonColour(self.buttonDictionary[person])
                    self.chatSelectAreaLayout.addStretch()
                    self.chatSelectArea.setWidget(self.chatSelectAreaWidget)
                    return

        if (self.chatSelectAreaLayout.itemAt(0) != None):
            self.setSelectedButtonColour(self.chatSelectAreaLayout.itemAt(0).widget())
            self.currentChatPerson = self.app.people[list(self.app.people.keys())[0]]
            self.chatSelectAreaLayout.addStretch()
            self.chatSelectArea.setWidget(self.chatSelectAreaWidget)
    def showNotExistError(self):
        #Show a dialog box if the user does not exist
        self.app.showError("User does not exist")

    def setSelectedButtonColour(self, button, oldButton=None):
        #set clicked on button to new style    
        button.setStyleSheet("""
        QPushButton {
            background-color: #455364;
            color: #ffffff;
            border: 2px solid #455364;
            border-radius: 10px;
            padding: 8px;
            font-size: 14px;
        }
        """)
        #remove style from current button
        if oldButton!=None and oldButton!=button:
            oldButton.setStyleSheet("""
            QPushButton {
                background-color: #19232D;
                color: #ffffff;
                border: 2px solid #455364;
                border-radius: 10px;
                padding: 8px;
                font-size: 14px;
            }
            """)   
    def setUnreadButtonColour(self, button):
        #set clicked on button to new style (red)    
        button.setStyleSheet("""
        QPushButton {
            background-color: #ff0000;
            color: #ffffff;
            border: 2px solid #455364;
            border-radius: 10px;
            padding: 8px;
            font-size: 14px;
        }
        """)                                                                
    def sendMessage(self):
        message = self.messageInput.toPlainText()
        #Check if message is valid before sending
        if self.validateMessage(message):
            newChatBubble = ChatBubble(message, True)
            self.addWithSpacer(newChatBubble)
            newChatBubble.adjustSizeToContent()
            self.currentChatPerson.appendChat(False, message)
            self.messageInput.clear()
            if self.app.encryptionEnabled:
                self.app.mainServer.messageRequest(message, self.currentChatPerson.userID,self.app.publicKey)
            else:
                self.app.mainServer.messageRequest(message, self.currentChatPerson.userID)
            self.app.mainServer.waitForContinue()
    def validateMessage(self, message):
        #Check if message is valid
        if len(message) > 0 and len(message) < 440:
            return True
        else:
            #Show a dialog box if the message is invalid
            self.app.showError("Message must be more than 0 and less than 440 characters")
            return False
    def addWithSpacer(self,item):
        self.scrollAreaLayout.removeItem(self.spacerItem)
        self.scrollAreaLayout.addWidget(item)
        self.scrollAreaLayout.addItem(self.spacerItem)
    def openChatWindow(self, person=None, senderID=None):
        self.scrollAreaLayout = QVBoxLayout()
        self.scrollAreaLayout.setAlignment(Qt.AlignCenter)
        self.scrollAreaWidget = QWidget()
        self.scrollAreaWidget.setLayout(self.scrollAreaLayout)
        #add spacer, this is to ensure chat bubbles don't fill the screen when they are created
        self.spacerItem = QSpacerItem(20, 10000, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.scrollAreaLayout.addItem(self.spacerItem)
        if person == None:
            #if person is not passed as an argument, then a message must have been recieved
            person = self.currentChatPerson
            #This means we should use the passed senderID to set the button colour red
            self.setUnreadButtonColour(self.buttonDictionary[senderID])
        #clear chat window
        #set current chat person, passing the new person 
        #and current person buttons as arguments
        self.setSelectedButtonColour(self.buttonDictionary[person.userID], self.buttonDictionary[self.currentChatPerson.userID])
        #change the current chat person to the selected person
        self.currentChatPerson = person
        #get the contents of the chats and add each one to the view
        chatContents = self.currentChatPerson.getChats()
        for chat in chatContents:
            newChatBubble = ChatBubble(chatContents[chat]["message"], not chatContents[chat]["received"])
            self.addWithSpacer(newChatBubble)
        self.scrollArea.setWidget(self.scrollAreaWidget)
        # For testing purposes, attempt to get the public key from the server
        if self.app.encryptionEnabled and self.currentChatPerson.publicKey == None:
            self.app.mainServer.getPublicKeyRequest(self.currentChatPerson.userID)
        #scroll to the bottom of the chat window
        self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().maximum())

    def openHelpWindow(self):
        self.helpWindow = helpWindow.HelpWindow()
        self.helpWindow.show()
    def openSettingsWindow(self):
        self.settingsWindow = settingsWindow.SettingsWindow(self.app)
        self.settingsWindow.show()
    def eventFilter(self, obj, event):
        #Check if the enter key is pressed in the message input
        if event.type() == QEvent.KeyPress and obj is self.messageInput:
            if event.key() == Qt.Key_Return and self.messageInput.hasFocus():
                #If the enter key is pressed, send the message
                self.sendMessage()
                return True
        return super().eventFilter(obj, event)

class ChatBubble(QWidget):
    # This class is used to create the chat bubble
    # It is a subclass of QWidget so we can add additional requirements to the base 
    # QTextEdit class
    def __init__(self, message, isSentByMe):
        super().__init__()
        self.message = message
        self.isSentByMe = isSentByMe
        self.initUI()

    def initUI(self):
        self.textEdit = QTextEdit()
        #Read only so user can't edit message
        self.textEdit.setReadOnly(True)
        self.textEdit.setFrameStyle(QTextEdit.NoFrame)
        self.textEdit.document().setDocumentMargin(10)
        #Set max width even if window is too large
        self.setMaximumWidth(700)
        self.setMinimumHeight(55)
        #Hide scroll bar on messages
        self.textEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit.viewport().setAutoFillBackground(False)
        #Set stylesheet depending on if message is sent by user
        if (self.isSentByMe):
            #Set colour to dark blue if sent by user
            self.textEdit.setStyleSheet("""
            QTextEdit {
                background-color: #19232D;
                color: #ffffff;
                border-radius: 10px;
                padding: 8px;
                font-size: 14px;
            }
            """)
        else:
            #Set colour to dark grey if sent by other user
            self.textEdit.setStyleSheet("""
            QTextEdit {
                background-color: #455364;
                color: #ffffff;
                border-radius: 10px;
                padding: 8px;
                font-size: 14px;
            }
            """)
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.textEdit)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.textEdit.setText(self.message)
        #If the height is too large, increase the size of the text box
        self.adjustSizeToContent()
        self.textEdit.document().documentLayout().documentSizeChanged.connect(self.adjustSizeToContent)

    def adjustSizeToContent(self):
        # Call this method after setting the text or on resize events
        docHeight = self.textEdit.document().size().height()
        # Set the minimum height of the text box to 55
        # Increase the height of the text box to fit the content
        # Add 20 to the height to account for padding
        newHeight = max(55, int(docHeight + 20))  
        self.setMinimumHeight(newHeight)

    def resizeEvent(self, event):
        self.adjustSizeToContent()
        super().resizeEvent(event)
    
