from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
class MainWindow(QWidget):
    messageReceived = pyqtSignal(str)
    def __init__(self, app):
        super().__init__()
        #set variable to acess passed through app object
        self.app = app
        self.initUI()

    def initUI(self):
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
 
        #create input box for chat messages
        self.messageInput = QTextEdit()
        self.messageInput.setPlaceholderText("Chat Message Here...")
        self.messageInput.setMaximumHeight(100)

        #create buttons
        self.sendButton = QPushButton('Send')
        self.settingButton = QPushButton('Settings')
        self.idButton = QPushButton('View ID')
        self.quitButton = QPushButton('Quit')
        self.helpButton = QPushButton('Help')

        #create layouts
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.sendButton)
        self.buttonLayout.addWidget(self.settingButton)

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
        for person in self.app.people:
            button = QPushButton(self.app.people[person].username)
            #call openChatWindow with the person object as an argument
            #this function will be implemented later
            button.clicked.connect(lambda _, person=self.app.people[person]: self.openChatWindow(person))
            self.chatSelectAreaLayout.addWidget(button)

