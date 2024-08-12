from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
#Use a QDialog to create a new window
class HelpWindow(QDialog):
    def __init__(self):
        super().__init__()
        #Set the theme to dark
        darkStylesheet = qdarkstyle.load_stylesheet_pyqt5()
        self.setStyleSheet(darkStylesheet)
        #Set the title and size of the window
        self.setWindowTitle("Help")
        self.setGeometry(100, 100, 300, 200)
        #Create a tab widget
        self.tabWidget = QTabWidget()
        self.tabWidget.addTab(SetupTab(), "Setup")
        self.tabWidget.addTab(UserTab(), "Adding a friend")
        self.tabWidget.addTab(MessageTab(), "Sending a Chat")
        #Create a layout and add the tab widget to it
        layout = QVBoxLayout()
        layout.addWidget(self.tabWidget)
        self.setLayout(layout)

class SetupTab(QWidget):
    def __init__(self):
        super().__init__()
        #Set a vertical layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        #Create a title label and set the font
        self.label = QLabel("Setup")
        self.label.setFont(QFont('Arial', 20))
        self.layout.addWidget(self.label)
        #Create a label for each step
        self.label = QLabel("1. Open the settings window by clicking the settings button in the bottom middle of the main window.")
        self.layout.addWidget(self.label)
        self.label = QLabel("2. Enter your username in the username text box.")
        self.layout.addWidget(self.label)
        self.label = QLabel("3. Enter the server IP address in the server IP text box.")
        self.layout.addWidget(self.label)
        self.label = QLabel("4. Enter the server port in the server port text box.")
        self.layout.addWidget(self.label)
        self.label = QLabel("5. Click the save button.")
        self.layout.addWidget(self.label)
        self.label = QLabel("6. The application will restart and connect to the server.")
        self.layout.addWidget(self.label)

class UserTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel("Adding a friend")
        self.label.setFont(QFont('Arial', 20))
        self.layout.addWidget(self.label)

        self.label = QLabel("1. Click the add user button in the top left of the screen")
        self.layout.addWidget(self.label)

        self.label = QLabel("2. Enter the userID of your friend in the text box.")
        self.layout.addWidget(self.label)

        self.label = QLabel("3. Click the OK button.")
        self.layout.addWidget(self.label)

        self.label = QLabel("4. Your friend will appear in the list of users.")
        self.layout.addWidget(self.label)

        self.label = QLabel("5. You can now send messages to your friend.")
        self.layout.addWidget(self.label)

        self.layout.addWidget(self.label)

class MessageTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel("Sending a Chat")
        self.label.setFont(QFont('Arial', 20))
        self.layout.addWidget(self.label)

        self.label = QLabel("1. Select the person you want to chat with in the left hand window.")
        self.layout.addWidget(self.label)

        self.label = QLabel("2. Type your message in the text box at the bottom of the screen.")
        self.layout.addWidget(self.label)

        self.label = QLabel("3. Click the send button.")
        self.layout.addWidget(self.label)

        self.label = QLabel("4. Your message will appear in the chat window.")
        self.layout.addWidget(self.label)

            