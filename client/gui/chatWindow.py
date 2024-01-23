import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from qdarkstyle import load_stylesheet_pyqt5
class MainWindow(QWidget):
    messageReceived = pyqtSignal(str)
    def __init__(self, app):
        super().__init__()
        #set variable to acess passed through app object
        self.app = app
        self.initUI()

    def initUI(self):
        #loading the dark theme, in the future this will be a setting
        darkStylesheet = load_stylesheet_pyqt5()
        self.setStyleSheet(darkStylesheet)
        self.setWindowTitle('Chat Window')
        #Set minimum width of window to make sure chat experience is consistent
        self.setGeometry(100, 100, 770, 700) 
        #QScrollarea to allow for scrollling through people list
        self.chatSelectArea = QScrollArea()
        self.chatSelectArea.setWidgetResizable(True)
        # vbox layout so new buttons are added vertically
        self.chatSelectAreaLayout = QVBoxLayout()
        self.chatSelectAreaWidget = QWidget()
        self.chatSelectAreaWidget.setLayout(self.chatSelectAreaLayout)
        self.chatSelectArea.setWidget(self.chatSelectAreaWidget)
        #create buttons for each person in people list
        self.createPeopleButtons()
        #add stretch to make sure buttons are at top of list
        self.chatSelectAreaLayout.addStretch()

        #create scroll area for chat messages
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaLayout = QVBoxLayout()
        self.scrollAreaLayout.setAlignment(Qt.AlignCenter)
        self.scrollAreaWidget = QWidget()
        self.scrollAreaWidget.setLayout(self.scrollAreaLayout)
        self.scrollArea.setWidget(self.scrollAreaWidget)

        #add spacer, this is to ensure chat bubbles don't fill the screen when they are created
        self.spacerItem = QSpacerItem(20, 10000, QSizePolicy.Minimum, QSizePolicy.Expanding)
        #create input box for chat messages
        self.messageInput = QTextEdit()
        self.messageInput.setPlaceholderText("Chat Message Here...")
        self.messageInput.setMaximumHeight(100)

        #create buttons
        self.sendButton = QPushButton('Send')
        self.sendButton.clicked.connect(lambda _,: self.sendMessage())
        self.settingButton = QPushButton('Settings')
        self.idButton = QPushButton('View ID')
        self.quitButton = QPushButton('Quit')
        #wtf is this
        self.quitButton.clicked.connect(lambda _,: os.system("pkill Python"))
        self.helpButton = QPushButton('Help')

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
        self.topLayout.addWidget(self.chatSelectArea,1)
        self.topLayout.addLayout(self.rightLayout,3)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.buttonLayout)
        
        self.setLayout(self.mainLayout)
    def createPeopleButtons(self):
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
            #this function will be implemented later
            button.clicked.connect(lambda _, person=self.app.people[person]: self.openChatWindow(person))
            self.chatSelectAreaLayout.addWidget(button)
        #adress dictionary based on order added to layout
        #this is so we can change the colour of the button when the user selects it
        self.setSelectedButtonColour(self.chatSelectAreaLayout.itemAt(0).widget())
        self.currentChatPerson = self.app.people[list(self.app.people.keys())[0]]
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
    def sendMessage(self):
        message = self.messageInput.toPlainText()
        newChatBubble = ChatBubble(message, True)
        self.addWithSpacer(newChatBubble)
        self.currentChatPerson.appendChat(False, message)
        #self.app.mainServer.messageRequest(message,self.currentChatPerson.userID)
    def addWithSpacer(self,item):
        self.scrollAreaLayout.removeItem(self.spacerItem)
        self.scrollAreaLayout.addWidget(item)
        self.scrollAreaLayout.addItem(self.spacerItem)
    def openChatWindow(self, person):
        #clear chat window
        self.clearChatWindow()
        #set current chat person
        self.setSelectedButtonColour(self.buttonDictionary[person.userID], self.buttonDictionary[self.currentChatPerson.userID])
        self.currentChatPerson = person
        chatContents = self.currentChatPerson.getChats()
        for chat in chatContents:
            newChatBubble = ChatBubble(chatContents[chat]["message"], not chatContents[chat]["recieved"])
            self.addWithSpacer(newChatBubble)
    def clearChatWindow(self):
        #clear chat window
        for i in range(self.scrollAreaLayout.count()-1):
            print(i)
            self.scrollAreaLayout.itemAt(i).widget().deleteLater()

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