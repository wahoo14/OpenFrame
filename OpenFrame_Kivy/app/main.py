from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.uix.filechooser import FileChooserListView
from kivy.metrics import dp
import re
# import psutil
import os
import random
import datetime
#mobile specific permissions
from kivy import platform
if platform == "android":
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
from android.storage import primary_external_storage_path


"""
Feature Backlog
DONE -configure time each photo is displayed
DONE -format buttons/screens
Doneinitial git repo
DONE -Configure order of photos (random vs. sequential)
DONE -Introductional Blurb/About page (add instructions)
DONE -Sleep feature for nighttime
DONE -improve error handling (HIDDEN THUMB DRIVE FILES)
-bundle as executable

-Display optional clock with toggle on/off
-overlay Frame
-Connect to other photo sources (AWS, GCP, DropBox, etc.)
-distribute software updates
-"End Play" button on config page
"""

class SplashScreen(Screen):
    """
    Initial landing page, Screen[0], 1st in workflow.
    Handle full screen in the buildozer.spec file
    """
    # Window.fullscreen = 'auto'
    pass

class DriveSelectScreen(Screen):
    pass
#     """
#     Screen[3], 2nd in workflow.  Used to select a drive from which to pull photos
#     NOT USED IN MOBILE DEVICE CODE BASE
#     """

#     def change_screen(self, instance):
#         self.manager.current = 'folderSelect'
#         self.manager.transition.direction = "left"
#         self.manager.screens[3].ids.selected_drive = instance.drive_id

#     def on_enter(self):
#         #early setting of sleepmode being active. this is a hack that should be revisited
#         self.manager.screens[6].ids.sleepModeActive = False
#         #NON PC VERSION
#         #functionality to detect available drives for the user to pick from
#         layout = self.ids.driveLayout
#         if layout.children:
#              None
#         else:
#             for drive_meta in psutil.disk_partitions():
#                  drive = drive_meta.device
#                  drive_btn = Button(text=drive, on_press=self.change_screen)
#                  drive_btn.drive_id = drive
#                  layout.add_widget(drive_btn)

class FolderSelectScreen(Screen):
    """
    Screen[1]: Folder select screen, 3rd in workflow.
    """
    selected_drive = StringProperty(0)
    
    def on_enter(self):
        """load and display folders from previously selected drive
        kivy limitation here regarding needing to double click to select 
        Currently using backend parsing/trimming along with front end hints
        to guide user input.
        """
        #NON PC VERSION
        # self.selected_drive = self.manager.screens[3].ids.selected_drive
        self.manager.screens[6].ids.sleepModeActive = False
        self.manager.screens[1].ids.selected_fpath = []
        layout = self.ids.folderSelect
        layout.clear_widgets()
        folderSelect = FileChooserListView(dirselect=True, path= primary_external_storage_path(), on_touch_down= self.on_select)
        layout.add_widget(folderSelect)        
    
    def on_select(self, instance, touch):
        """
        called when a folder/filed is clicked, in the on_enter function in this class.
        """
        self.ids.selectedFolderLabel.text = str(instance.selection)
        self.manager.screens[1].ids.selected_fpath = instance.selection

    def continue_pressed(self):
        """
        Called on Continue button clicked.
        """
        #NON PC VERSION
        if not self.manager.screens[1].ids.selected_fpath:
             self.manager.screens[1].ids.selected_fpath.append(self.selected_drive)
        pass
             
class AdditionalOptionsScreen(Screen):
    """
    Screen[5], 4th in workflow.  Used to select additional options for display configuration
    """
    
    def __init__(self, **kwargs):  
        super().__init__(**kwargs)
        """
        Configure initial variables
        """
        self.ids.sleep_mode_active = False
        self.ids.sequence = "Random"

    def on_enter(self):
        """
        Configure additional variables as well as set corresponding UI elements values
        """
        if self.ids.sequence == "Random":
            self.ids.random.active = True
            self.ids.sequential.active = False
        elif self.ids.sequence == "Sequential":
            self.ids.sequential.active = True
            self.ids.random.active = False

        if self.ids.sleep_mode_active == False:
            self.ids.off.active = True
        else:
            self.ids.on.active = True
    
    def order_display_checkbox_click(self, instance, value, display_order):
        """
        Function governing the display order checkbox UI
        """
        if value == True:
            self.manager.screens[5].ids.displayOrder = display_order
            self.ids.sequence = display_order

    def sleep_mode_select(self, instance, value, selected):
        """
        Function supporting the sleep mode selection button
        """
        if value == True:
            if selected == "On":
                self.ids.sleepOn0.opacity = 1
                self.ids.sleepOn0.width = self.ids.sleepOn0.texture_size[0] + dp(75)
                self.ids.sleepOn1.opacity = 1
                self.ids.sleepOn2.opacity = 1
                self.ids.sleepOn3.opacity = 1
                self.ids.sleepOn4.opacity = 1
                self.ids.sleep_mode_active = True
            else:
                self.ids.sleepOn0.opacity = 0
                self.ids.sleepOn0.width = 0
                self.ids.sleepOn1.opacity = 0
                self.ids.sleepOn2.opacity = 0
                self.ids.sleepOn3.opacity = 0
                self.ids.sleepOn4.opacity = 0
                self.ids.sleep_mode_active = False
        
    def on_play(self):
        """
        Function called on play; saves variable values as well as validates a sleep mode
        has been selected if the option is selected.
        """
        self.manager.screens[5].ids.photoDisplaySeconds = self.ids.photoDisplayTime.text
        if self.ids.sleep_mode_active == True:
            if self.manager.screens[5].ids.sleepOn2.text == "":
                self.manager.screens[5].ids.sleepNotConfiguredValidation.opacity = 1
            elif self.manager.screens[5].ids.sleepOn4.text == "":
                self.manager.screens[5].ids.sleepNotConfiguredValidation.opacity = 1
            else:
                self.manager.current = "display"
        else:
            self.manager.screens[5].ids.sleepNotConfiguredValidation.opacity = 0
            self.manager.current = "display"

    def on_back(self):
        pass

class SleepTimeSelectScreen(Screen):
    """
    Screen[6], optional in workflow.  Used to designate optional sleep mode start and stop times
    """

    def validate_time_input(self, user_input):
        """
        Function using regex to validate the users input time matches a HH:MM format following the
        24 hour clock.
        """
        time_input_regex = r"(?:[01]\d|2[0-3]):(?:[0-5]\d)"
        if re.match(time_input_regex, user_input):
            return True
        else:
            return False

    def on_enter(self):
        """
        Function called on enter, makes validation messages disappear.
        """
        self.ids.sleepStartValidationMessage.opacity = 0
        self.ids.sleepEndValidationMessage.opacity = 0
        
    def save_sleep_timer(self):
        """
        Function called when the user clicks save on the sleep mode input screen.
        Handles cases when validation has been popped on one, both or neither user input
        times.
        """
        #both True
        if self.validate_time_input(self.ids.sleepStartTime.text) == True and self.validate_time_input(self.ids.sleepEndTime.text) == True:
            self.manager.screens[6].ids.sleepStart = self.ids.sleepStartTime.text
            self.manager.screens[6].ids.sleepEnd = self.ids.sleepEndTime.text
            self.manager.screens[6].ids.sleepModeActive = True
            self.manager.screens[5].ids.sleepOn2.text = self.ids.sleepStartTime.text
            self.manager.screens[5].ids.sleepOn4.text = self.ids.sleepEndTime.text
            self.ids.sleepStartValidationMessage.opacity = 0
            self.ids.sleepEndValidationMessage.opacity = 0
            self.manager.current = "additionalOptions"
        #one false
        elif self.validate_time_input(self.ids.sleepStartTime.text) == False and self.validate_time_input(self.ids.sleepEndTime.text) == True:
            self.ids.sleepStartValidationMessage.opacity = 1
            self.ids.sleepEndValidationMessage.opacity = 0
            self.manager.screens[6].ids.sleepModeActive = False
        #one false
        elif self.validate_time_input(self.ids.sleepStartTime.text) == True and self.validate_time_input(self.ids.sleepEndTime.text) == False:
            self.ids.sleepStartValidationMessage.opacity = 0
            self.ids.sleepEndValidationMessage.opacity = 1
            self.manager.screens[6].ids.sleepModeActive = False
        #both false
        elif self.validate_time_input(self.ids.sleepStartTime.text) == False and self.validate_time_input(self.ids.sleepEndTime.text) == False:
            self.ids.sleepStartValidationMessage.opacity = 1
            self.ids.sleepEndValidationMessage.opacity = 1
            self.manager.screens[6].ids.sleepModeActive = False

class DisplayScreen(Screen):  
    """
    Screen[4], final step in workflow. Actually displays photos.
    """

    def parse_input_time(self, input_time):
        """
        Transforms user input text time into pythonic time.
        """
        clock_time = datetime.time(int(input_time.split(":")[0]), int(input_time.split(":")[1]))
        return clock_time
    
    def on_enter(self):
        """
        Function called on enter: sets random vs sequential variables, as well as cleans the 
        user's selected filepaths to ensure a folder has been selected, and that files with non
        photo (JPG, JPEG, PNG) file extensions are pruned.  Finally initiates the photo display
        by calling the Kivy clock function to update the image widget on the user's selected time
        """
        self.photo_incrementor = 0
        if self.manager.screens[5].ids.displayOrder == "Random":
            self.displayRandom = True
        else:
            self.displayRandom = False

        #test if dir, if not trim to directory path
        self.selected_fpath = self.manager.screens[1].ids.selected_fpath[0]
        if os.path.isdir(self.selected_fpath):
            pass
        else:
            self.selected_fpath = os.path.dirname(self.selected_fpath)

        #get list of fpaths
        self.fpath_list = []
        for dirpath, _, photos in os.walk(self.selected_fpath):
            for photo in sorted(photos):
                photo_fpath = os.path.abspath(os.path.join(dirpath, photo))
                self.fpath_list.append(photo_fpath) 
        #clean file list
        self.cleaned_list = []
        for x in self.fpath_list:
            if x.lower().endswith(('.png', '.jpg', '.jpeg')):
                self.cleaned_list.append(x)

        if self.displayRandom:
            self.im = Image(source="", allow_stretch= False, keep_ratio= True, color = [0,0,0,0])
            self.add_widget(self.im)
            Clock.schedule_interval(self.update_photo_random, int(self.manager.screens[5].ids.photoDisplaySeconds))
        else:
            self.im = Image(source="", allow_stretch= False, keep_ratio= True, color = [0,0,0,0])
            self.add_widget(self.im)
            Clock.schedule_interval(self.update_photo_sequential, int(self.manager.screens[5].ids.photoDisplaySeconds))

    def update_photo_random(self, interval):
        """
        Function called when the user has opted to display the photos in random order.
        Randomly selects a photo from the list generated from the selected users drive/directory for display.
        Accounts for if sleep mode has been selected or not by setting the image source to null and blacking the display.
        """
        if self.manager.screens[6].ids.sleepModeActive:
            sleep_start = self.parse_input_time(self.manager.screens[6].ids.sleepStart)
            sleep_end = self.parse_input_time(self.manager.screens[6].ids.sleepEnd)
            now = datetime.datetime.now()
            now_time = now.time()
            if now_time >= sleep_start and now_time <= sleep_end:
                self.im.color = [0,0,0,0]
                self.im.source = ""
            else:
                self.im.color = [1,1,1,1]
                self.im.source = random.choice(self.cleaned_list)
        else:
            self.im.color = [1,1,1,1]
            self.im.source = random.choice(self.cleaned_list)
        
    def update_photo_sequential(self, interval):
        """
        Function called when the user has selected to display the photos in ordered sequence.  Accounts for sleep mode
        by setting image source to null and blackening the dispaly when required.  Also contains logic to loop the incrementor 
        back to zero when it has reached the end of the photo list's length.
        """
        if self.photo_incrementor >= len(self.cleaned_list):
            self.photo_incrementor = 0
        if self.manager.screens[6].ids.sleepModeActive:
            sleep_start = self.parse_input_time(self.manager.screens[6].ids.sleepStart)
            sleep_end = self.parse_input_time(self.manager.screens[6].ids.sleepEnd)
            now = datetime.datetime.now()
            now_time = now.time()   
            if now_time >= sleep_start and now_time <= sleep_end:
                self.im.source = ""
                self.im.color = [0,0,0,0]
            else:
                self.im.color = [1,1,1,1]
                self.im.source = self.cleaned_list[self.photo_incrementor]
                self.photo_incrementor+=1
        else:
            self.im.color = [1,1,1,1]
            self.im.source = self.cleaned_list[self.photo_incrementor]
            self.photo_incrementor+=1

class AboutScreen(Screen):
    """
    features explanatory text, Screen[2], workflow optional
    """
    pass

class OpenFrame(App):
    """
    Parent Kivy app class
    """
    def on_start(self, **kwargs):
        #mobile only function
        if platform == "android":
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])

if __name__ == '__main__':
    OpenFrame().run()