from re import sub
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.QtGui import QPixmap, QColor
from os.path import expanduser
import os
import random
from datetime import datetime, time

timer = QtCore.QTimer()
#todo, get rid of global variables
sleepModeActive=None
sleepTimeStart=None
sleepTimeEnd=None

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
        self.stack3 = QtWidgets.QWidget()

        self.splashPageUI()
        self.configScreenUI()
        self.aboutScreenUI()

        self.QtStack.addWidget(self.stack1)
        self.QtStack.addWidget(self.stack2)
        self.QtStack.addWidget(self.stack3)

    def splashPageUI(self):
        #configuration for initial splash page
        self.splashCoord_x = self.stack1.pos().x()
        self.splashCoord_y = self.stack1.pos().y()

        self.stack1.resize(800, 480)
        self.stack1.setStyleSheet("background: lightGrey")
        grid = QtWidgets.QGridLayout()
        self.stack1.setLayout(grid)
        grid.setRowStretch(0, 4)
        grid.setRowStretch(1, 1)
        grid.setRowStretch(2, 4)

        #Splash text config
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        splashTitle = QtWidgets.QLabel(self.stack1)
        splashTitle.setFont(font)
        grid.addWidget(splashTitle, 0, 0, QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)
        splashTitle.setText("Welcome to OpenFrame")

        #splash about text
        splashAboutText = QtWidgets.QLabel(self.stack1)
        splashAboutText.setText("Enjoy your photo collection through a customizable, open-source digital picture frame")
        splashAboutText.setContentsMargins(0,0,0,0)
        grid.addWidget(splashAboutText, 1, 0, QtCore.Qt.AlignCenter)

        #button layout + about button config
        buttonLayout = QtWidgets.QGridLayout()
        grid.addLayout(buttonLayout,2,0)
        self.splashAboutButton = QtWidgets.QPushButton(self.stack1)
        self.splashAboutButton.setText("About")
        buttonLayout.addWidget(self.splashAboutButton, 0, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)

        #continue button config
        self.splashContinueButton = QtWidgets.QPushButton(self.stack1)
        self.splashContinueButton.setText("Continue")
        buttonLayout.addWidget(self.splashContinueButton, 0, 1, QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)

    def configScreenUI(self):
        #configuration screen config
        self.configCoord_x = self.stack2.pos().x()
        self.configCoord_y = self.stack2.pos().y()

        self.stack2.resize(800, 480)
        self.stack2.setStyleSheet("background: lightGrey")
        grid = QtWidgets.QGridLayout()
        sub_grid = QtWidgets.QGridLayout()
        grid.addLayout(sub_grid, 1, 1)
        self.stack2.setLayout(grid)

        #config for page header
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        configTitle = QtWidgets.QLabel(self.stack2)
        configTitle.setFont(font)
        grid.addWidget(configTitle, 0, 1, QtCore.Qt.AlignCenter)
        configTitle.setText("Configure Your Digital Picture Frame")

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
        self.photoDisplayTimeInput.setText("5")
        onlyInt = QtGui.QIntValidator()
        onlyInt.setRange(0, 4)
        self.photoDisplayTimeInput.setValidator(onlyInt)
        self.photoDisplayTimeInput.setFixedSize(120,20)
        sub_grid.addWidget(self.photoDisplayTimeInput, 2, 1, QtCore.Qt.AlignLeft)

        #config for photo display pattern
        self.selectedPhotoDisplayMode = QtWidgets.QLabel(self.stack2)
        self.selectedPhotoDisplayMode.setText("How Would You Like Your Photos Displayed?")
        sub_grid.addWidget(self.selectedPhotoDisplayMode, 3, 0, QtCore.Qt.AlignRight)

        #config for photo display pattern input
        buttonGroupDisplayPatternInput = QtWidgets.QButtonGroup(self)
        radioLayoutOrder = QtWidgets.QGridLayout()
        self.selectedPhotoDisplayModeInputRandom = QtWidgets.QRadioButton("Random")
        self.selectedPhotoDisplayModeInputRandom.setChecked(True)
        radioLayoutOrder.addWidget(self.selectedPhotoDisplayModeInputRandom, 0, 0)
        self.selectedPhotoDisplayModeInputSequential = QtWidgets.QRadioButton("Sequential")
        radioLayoutOrder.addWidget(self.selectedPhotoDisplayModeInputSequential, 0, 1)
        buttonGroupDisplayPatternInput.addButton(self.selectedPhotoDisplayModeInputRandom)
        buttonGroupDisplayPatternInput.addButton(self.selectedPhotoDisplayModeInputSequential)
        sub_grid.addLayout(radioLayoutOrder,3,1,QtCore.Qt.AlignLeft)

        #commented out until I know how to do this
        #config for clock display
        # self.clockConfig = QtWidgets.QLabel(self.stack2)
        # self.clockConfig.setText("Display Clock?")
        # sub_grid.addWidget(self.clockConfig, 4, 0, QtCore.Qt.AlignRight)

        # #config for clock display input
        # buttonGroupClockConfigInput = QtWidgets.QButtonGroup(self)
        # radioLayoutClock = QtWidgets.QGridLayout()
        # self.clockConfigInputOff = QtWidgets.QRadioButton("Off")
        # self.clockConfigInputOff.setChecked(True)
        # radioLayoutClock.addWidget(self.clockConfigInputOff, 0, 0)
        # self.clockConfigInputOn = QtWidgets.QRadioButton("On")
        # radioLayoutClock.addWidget(self.clockConfigInputOn, 0, 1)
        # buttonGroupClockConfigInput.addButton(self.clockConfigInputOff)
        # buttonGroupClockConfigInput.addButton(self.clockConfigInputOn)
        # sub_grid.addLayout(radioLayoutClock,4,1,QtCore.Qt.AlignLeft)

        # config sleep option
        self.sleepConfig = QtWidgets.QLabel(self.stack2)
        self.sleepConfig.setText("Sleep Mode "+ u"\U0001F6C8")
        sub_grid.addWidget(self.sleepConfig, 4, 0, QtCore.Qt.AlignRight)
        self.sleepConfig.setToolTip("Enabling sleep mode will darken the screen between user-specified hours")

        #config for sleep mode input
        buttonGroupSleepConfigInput = QtWidgets.QButtonGroup(self)
        radioLayoutSleep = QtWidgets.QGridLayout()
        self.clockSleepInputOff = QtWidgets.QRadioButton("Off")
        self.clockSleepInputOff.setChecked(True)
        radioLayoutSleep.addWidget(self.clockSleepInputOff, 0, 1)
        self.clockSleepInputOn = QtWidgets.QRadioButton("On")
        radioLayoutSleep.addWidget(self.clockSleepInputOn, 0, 0)
        buttonGroupSleepConfigInput.addButton(self.clockSleepInputOff)
        buttonGroupSleepConfigInput.addButton(self.clockSleepInputOn)
        sub_grid.addLayout(radioLayoutSleep,4,1,QtCore.Qt.AlignLeft)
        self.clockSleepInputOff.toggled.connect(self.sleepTimeSelectDisplay)
        self.clockSleepInputOn.toggled.connect(self.sleepTimeSelectDisplay)

        #sleep time input config
        #parent widget
        self.sleepTimeParentWidget = QtWidgets.QWidget(self)
        self.subTimeConfigLayout = QtWidgets.QGridLayout()
        self.sleepTimeParentWidget.setLayout(self.subTimeConfigLayout)
        #timeselect widgets
        #start
        self.sleepStartLabel = QtWidgets.QLabel(self)
        self.sleepStartLabel.setText("Start Time")
        self.subTimeConfigLayout.addWidget(self.sleepStartLabel,0,0, QtCore.Qt.AlignTop)
        self.sleepTimeStart = QtWidgets.QTimeEdit(self)
        self.sleepTimeStart.setTime(QtCore.QTime(21, 0, 0))
        self.subTimeConfigLayout.addWidget(self.sleepTimeStart,0,1, QtCore.Qt.AlignTop)
        #end
        self.sleepEndLabel = QtWidgets.QLabel(self)
        self.sleepEndLabel.setText("End Time")
        self.subTimeConfigLayout.addWidget(self.sleepEndLabel,1,0, QtCore.Qt.AlignTop)
        self.sleepTimeEnd = QtWidgets.QTimeEdit(self)
        self.subTimeConfigLayout.addWidget(self.sleepTimeEnd,1,1, QtCore.Qt.AlignTop)
        self.sleepTimeEnd.setTime(QtCore.QTime(7, 0, 0))
        #add time into parent layout
        sub_grid.addWidget(self.sleepTimeParentWidget,5,1,QtCore.Qt.AlignLeft)
        self.sleepTimeParentWidget.hide()

        #config for back button
        self.configureBackButton = QtWidgets.QPushButton(self.stack2)
        self.configureBackButton.setText("Back")
        grid.addWidget(self.configureBackButton, 6, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)    
        
        #config for continue/Play button
        self.configureContinueButton = QtWidgets.QPushButton(self.stack2)
        self.configureContinueButton.setText("Play")
        self.configureContinueButton.setEnabled(False)
        grid.addWidget(self.configureContinueButton, 6, 3, QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)
        self.configureContinueButton.clicked.connect(self.playButtonClicked)

    def sleepTimeSelectDisplay(self):
        if self.clockSleepInputOff.isChecked():
            self.sleepTimeParentWidget.hide()
        elif self.clockSleepInputOn.isChecked():
            self.sleepTimeParentWidget.show()

    def playButtonClicked(self):
        #function called from the configuration screen to set configured variables and display the photos loop popup screen
        self.photoDisplayWindow.photosFolderSecondWindow = self.photosFolder
        self.photoDisplayInterval = int(self.photoDisplayTimeInput.text())*1000
        timer.setInterval(self.photoDisplayInterval)

        #handle photo display mode selection
        if self.selectedPhotoDisplayModeInputRandom.isChecked() == True:
            self.photoDisplayWindow.displayRandom()
        elif self.selectedPhotoDisplayModeInputSequential.isChecked() == True:
            self.photoDisplayWindow.displaySequential()

        # #handle clock config selection
        # if self.clockConfigInputOff.isChecked() == True:
        #     None
        # elif self.clockConfigInputOn.isChecked() == True:
        #     self.photoDisplayWindow.displayClock()

        #handle sleep mode input selection
        #if anyone ever reads this, i realize this is not good architecture but i didnt want to redo everything...
        if self.clockSleepInputOff.isChecked() == True:
            global sleepModeActive 
            sleepModeActive= False
        elif self.clockSleepInputOn.isChecked() == True:
            sleepModeActive= True
            global sleepTimeStart 
            sleepTimeStart = self.sleepTimeStart.time()
            global sleepTimeEnd
            sleepTimeEnd = self.sleepTimeEnd.time()
        
        self.stack2.close()

    def folderBrowserClicked(self):
        #function to handle the photos directory selection once the "browse" button is clicked
        self.photosFolder = QFileDialog.getExistingDirectory(self.stack2, "Select Directory", expanduser("~"), QFileDialog.ShowDirsOnly)
        # sender = self.sender()
        self.directorySelectButton.setText(self.photosFolder)
        self.configureContinueButton.setEnabled(True)

    def aboutScreenUI(self):
        #about screen config
        self.aboutCoord_x = self.stack3.pos().x()
        self.aboutCoord_y = self.stack3.pos().y()
        self.stack3.resize(800, 480)
        self.stack3.setStyleSheet("background: lightGrey")
        self.aboutGrid = QtWidgets.QGridLayout()
        self.stack3.setLayout(self.aboutGrid)

        #config for page header
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.aboutTitle = QtWidgets.QLabel(self.stack3)
        self.aboutTitle.setFont(font)
        self.aboutGrid.addWidget(self.aboutTitle, 0, 0, QtCore.Qt.AlignCenter)
        self.aboutTitle.setText("About OpenFrame")

        # config for about body text
        ##TODO
        self.aboutText = QtWidgets.QLabel(self.stack3)
        self.aboutText.setText("OpenFrame is an open-source digital picture frame made so that anyone can enjoy the library of photos they've taken.  The code repository is available online at https://github.com/wahoo14/OpenFrame")
        self.aboutText.setWordWrap(True)
        self.aboutGrid.addWidget(self.aboutText, 1, 0, QtCore.Qt.AlignCenter)

        #about back button
        self.aboutBackButton = QtWidgets.QPushButton(self.stack3)
        self.aboutBackButton.setText("Back")
        self.aboutGrid.addWidget(self.aboutBackButton, 2, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)   

class pictureDisplayWindow(QtWidgets.QWidget):
    #class called to instantiate the photos display window
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

        #creates widget to contain and display the photos
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

    def displaySequential(self):
        #function called to display the photos window and sequentially loop through the selected directory's photos based on the timer's timeout
        self.fpath_list = []
        for dirpath, _, photos in os.walk(self.photosFolderSecondWindow):
            for photo in photos:
                photo_fpath = os.path.abspath(os.path.join(dirpath, photo))
                self.fpath_list.append(photo_fpath)     
        # self.timer.timeout.connect(lambda: self.updatePhoto([x for x in self.fpath_list]))
        self.photoIncrementor = 0
        self.timer.timeout.connect(lambda: self.updatePhoto(self.displaySequentialSubFunction()))
        self.showMaximized()

    def displaySequentialSubFunction(self):
        try:
            photo_fpath = self.fpath_list[self.photoIncrementor]
        except:
            self.photoIncrementor = 0
            photo_fpath = self.fpath_list[self.photoIncrementor]
        self.photoIncrementor+=1

        return photo_fpath

    def displayRandom(self):
        #function called to display the photos window and randomly loop through the selected directory's photos based on the timer's timeout
        self.fpath_list = []
        for dirpath, _, photos in os.walk(self.photosFolderSecondWindow):
            for photo in photos:
                photo_fpath = os.path.abspath(os.path.join(dirpath, photo))
                self.fpath_list.append(photo_fpath)        
        self.timer.timeout.connect(lambda: self.updatePhoto(random.choice(self.fpath_list)))
        self.showMaximized()

    def updatePhoto(self, photo_fpath):
        #function called to update the photo currently being displayed
        #adding in logic for sleep config
        if sleepModeActive==True:
            if QtCore.QTime.currentTime() >= sleepTimeStart and QtCore.QTime.currentTime() < sleepTimeEnd:
                self.img_widget.setPixmap(self.pixmap)
            else:
                self.img_widget.setPixmap(QtGui.QPixmap(photo_fpath).scaled(self.screen_width, self.screen_height, QtCore.Qt.KeepAspectRatio))
        else:
            self.img_widget.setPixmap(QtGui.QPixmap(photo_fpath).scaled(self.screen_width, self.screen_height, QtCore.Qt.KeepAspectRatio))


        