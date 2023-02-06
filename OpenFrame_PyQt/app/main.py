from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from Ui_Main import Ui_Main

"""
Feature Backlog
DONE -configure time each photo is displayed
DONE -implement config back button
DONE -initial git repo
DONE -open windows at same coordinates
DONE -Configure order of photos (random vs. sequential)
IN PROGRESS-Introductional Blurb/About page
DONE -Sleep feature for nighttime
-bundle as executable
-improve error handling

-Display optional clock with toggle on/off
-overlay Frame
-Connect to other photo sources (AWS, GCP, DropBox, etc.)
-distribute software updates
-"End Play" button on config page
"""

class Main(QMainWindow, Ui_Main):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)

        self.splashContinueButton.clicked.connect(self.splashContinueButtonHandler)
        self.configureBackButton.clicked.connect(self.configBackButtonHandler)
        self.splashAboutButton.clicked.connect(self.splashAboutButtonHandler)
        self.aboutBackButton.clicked.connect(self.aboutBackButtonHandler)

    def configBackButtonHandler(self):
        self.QtStack.setCurrentIndex(0)
        x=self.stack2.pos().x()
        y=self.stack2.pos().y()
        self.stack1.move(x, y)

    def splashContinueButtonHandler(self):
        self.QtStack.setCurrentIndex(1)
        x=self.stack1.pos().x()
        y=self.stack1.pos().y()
        self.stack2.move(x, y)

    def splashAboutButtonHandler(self):
        self.QtStack.setCurrentIndex(2)
        x=self.stack1.pos().x()
        y=self.stack1.pos().y()
        self.stack3.move(x, y)

    def aboutBackButtonHandler(self):
        self.QtStack.setCurrentIndex(0)
        x=self.stack3.pos().x()
        y=self.stack3.pos().y()
        self.stack1.move(x, y)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    showMain = Main()
    sys.exit(app.exec_())