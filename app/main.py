from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from Ui_Main import Ui_Main

"""
Feature Backlog
DONE -time each photo is displayed
DONE -implement config back button
-Git repo
-open windows at same coordinates
-Introductional Blurb/About page
-"End Play" button on config page
-Configure order of photos (random vs. sequential)
-Display optional clock with toggle on/off
-Save configuration settings + autoplay
-Sleep feature for nighttime
-improve error handling
-overlay Frame
-Connect to other photo sources (AWS, GCP, DropBox, etc.)
-distribute software updates
"""

class Main(QMainWindow, Ui_Main):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)

        self.splashContinueButton.clicked.connect(self.OpenWindow1)
        self.configureBackButton.clicked.connect(self.configBackButton)

    def OpenWindow1(self):
        self.QtStack.setCurrentIndex(1)
    
    def configBackButton(self):
        self.QtStack.setCurrentIndex(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    showMain = Main()
    sys.exit(app.exec_())