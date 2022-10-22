from re import sub
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.QtGui import QPixmap, QColor
from os.path import expanduser
import os
import random

timer = QtCore.QTimer()

class Ui_Main(QtWidgets.QWidget):
    def setupUi(self, Main):
        #set up stacked widget containing multiple pages
        Main.setObjectName("Main")
        Main.resize(800, 480)
        self.photosFolder = None
        self.photoDisplayInterval = None
        self.photoDisplayWindow = pictureDisplayWindow()

        self.QtStack = QtWidgets.QStackedLayout()

        self.stack1 = QtWidgets.QWidget()
        self.stack2 = QtWidgets.QWidget()

        self.Window1UI()
        self.Window2UI()

        self.QtStack.addWidget(self.stack1)
        self.QtStack.addWidget(self.stack2)

    def Window1UI(self):
        #configuration for initial splash page
        self.stack1.resize(800, 480)
        self.stack1.setStyleSheet("background: lightGrey")
        grid = QtWidgets.QGridLayout()
        self.stack1.setLayout(grid)

        #Splash text config
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.title = QtWidgets.QLabel(self.stack1)
        self.title.setFont(font)
        grid.addWidget(self.title, 0, 0, QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)
        self.title.setText("Welcome to OpenFrame")

        #splash about text config
        self.splashAboutText = QtWidgets.QLabel(self.stack1)
        self.splashAboutText.setText("Lorem Ipsum")
        grid.addWidget(self.splashAboutText, 1, 0, QtCore.Qt.AlignCenter)

        #continue button config
        self.splashContinueButton = QtWidgets.QPushButton(self.stack1)
        self.splashContinueButton.setText("Continue")
        grid.addWidget(self.splashContinueButton, 2, 0, QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)


    def Window2UI(self):
        #configuration screen config
        self.stack2.resize(800, 480)
        self.stack2.setStyleSheet("background: lightGrey")
        self.grid = QtWidgets.QGridLayout()
        sub_grid = QtWidgets.QGridLayout()
        self.grid.addLayout(sub_grid, 1, 1)
        self.stack2.setLayout(self.grid)

        #config for page header
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.title = QtWidgets.QLabel(self.stack2)
        self.title.setFont(font)
        self.grid.addWidget(self.title, 0, 1, QtCore.Qt.AlignCenter)
        self.title.setText("Configure Your Digital Picture Frame")

        #config for photos select label
        self.selectedFolder = QtWidgets.QLabel(self.stack2)
        self.selectedFolder.setText("Browse Photos Folder")
        sub_grid.addWidget(self.selectedFolder, 1, 0, QtCore.Qt.AlignRight)

        #config for photos select button
        self.directorySelectButton = QtWidgets.QPushButton(self.stack2)
        self.directorySelectButton.setText("No Folder Selected")
        self.directorySelectButton.setFixedSize(120,20)
        sub_grid.addWidget(self.directorySelectButton, 1, 1, QtCore.Qt.AlignLeft)
        self.directorySelectButton.clicked.connect(self.folderBrowserClicked)

        #config for timer select label
        self.selectedPhotoDisplayTime = QtWidgets.QLabel(self.stack2)
        self.selectedPhotoDisplayTime.setText("Select Display Time per Photo In Seconds")
        sub_grid.addWidget(self.selectedPhotoDisplayTime, 2, 0, QtCore.Qt.AlignRight)

        #config for timer select input
        self.photoDisplayTimeInput = QtWidgets.QLineEdit(self.stack2)
        self.photoDisplayTimeInput.setText("3")
        onlyInt = QtGui.QIntValidator()
        onlyInt.setRange(0, 4)
        self.photoDisplayTimeInput.setValidator(onlyInt)
        self.photoDisplayTimeInput.setFixedSize(120,20)
        sub_grid.addWidget(self.photoDisplayTimeInput, 2, 1, QtCore.Qt.AlignLeft)

        #config for back button
        self.configureBackButton = QtWidgets.QPushButton(self.stack2)
        self.configureBackButton.setText("Back")
        self.grid.addWidget(self.configureBackButton, 3, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)    
        
        #config for continue/Play button
        self.configureContinueButton = QtWidgets.QPushButton(self.stack2)
        self.configureContinueButton.setText("Play")
        self.configureContinueButton.setEnabled(False)
        self.grid.addWidget(self.configureContinueButton, 3, 3, QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)
        self.configureContinueButton.clicked.connect(self.playButtonClicked)

    def playButtonClicked(self):
        #function called from the configuration screen to set configured variables and display the photos loop popup screen
        self.photoDisplayWindow.photosFolderSecondWindow = self.photosFolder
        self.photoDisplayInterval = int(self.photoDisplayTimeInput.text())*1000
        timer.setInterval(self.photoDisplayInterval)
        self.photoDisplayWindow.display()

    def folderBrowserClicked(self):
        #function to handle the photos directory selection once the "browse" button is clicked
        self.photosFolder = QFileDialog.getExistingDirectory(self.stack2, "Select Directory", expanduser("~"), QFileDialog.ShowDirsOnly)
        sender = self.sender()
        self.directorySelectButton.setText(self.photosFolder)
        self.configureContinueButton.setEnabled(True)


class pictureDisplayWindow(QtWidgets.QWidget):
    #class called to instantiate the photos dispaly window
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        #intial configuration
        self.photosFolderSecondWindow = None
        self.photoDisplayInterval = None

        #config to get the available screen size
        #note- this might be redundant with the calling of the .displayMaximized() function...
        self.grid_2 = QtWidgets.QGridLayout()
        self.app = QApplication.instance()
        self.selected_screen = 0
        self.screens_available = self.app.screens()
        self.screen = self.screens_available[self.selected_screen]
        self.screen_width = self.screen.size().width()
        self.screen_height = self.screen.size().height()

        self.pixmap = QPixmap(self.screen_width, self.screen_height)
        self.pixmap.fill(QColor('black'))

        #creates widget to contain and dispaly the photos
        self.img_widget = QtWidgets.QLabel(self)
        self.img_widget.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowDoesNotAcceptFocus | QtCore.Qt.WindowStaysOnTopHint)
        self.img_widget.setCursor(QtCore.Qt.BlankCursor)       
        self.img_widget.setStyleSheet("background-color: black;") 

        self.img_widget.setGeometry(0, 0, self.screen_width, self.screen_height)  
        self.img_widget.setWindowTitle('OpenFrame')
        self.grid_2.addWidget(self.img_widget, 0, 0)
        self.img_widget.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)                
        self.img_widget.setPixmap(self.pixmap)
        self.img_widget.setText("")

        #timer apparently needs to be called within the init function of a class.  Have it tied to a
        #timer var outside both classes so that it can be updated from the child class photoDisplayWindow
        self.timer = timer
        self.timer.start(3000)


    def display(self):
        #function called to display the photos window and loop through the selected directory's photos based on the timer's timeout
        self.fpath_list = []
        for dirpath, _, photos in os.walk(self.photosFolderSecondWindow):
            for photo in photos:
                photo_fpath = os.path.abspath(os.path.join(dirpath, photo))
                self.fpath_list.append(photo_fpath)        
        self.timer.timeout.connect(lambda: self.updatePhoto(random.choice(self.fpath_list)))
        self.showMaximized()

    def updatePhoto(self, photo_fpath):
        #function called to update the photo currently being displayed
        self.img_widget.setPixmap(QtGui.QPixmap(photo_fpath).scaled(self.screen_width, self.screen_height, QtCore.Qt.KeepAspectRatio))
