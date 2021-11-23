###
# Import Python libraries
###
import PySimpleGUI as sg # pip install pysimplegui
from os import mkdir, path # List directory contents, make directory and path for checking if files/paths exist


###
# Import other files
###
from Files import Files # Class with functions for handling files
import mainWindow # Contains a function for opening the main window

###
# Load config file
###
config = Files.checkConfig()
if not config: # If config is empty (Failed to load config from file)
    config = Files.checkConfig(True) # Reset config

###
# Ask user for a directory and check it for saved files
### 
saveLocation = Files.changeSaveLocation(config)

if saveLocation is None: # No path to saved files
    sg.popup(title="Error", custom_text="No directory selected. Quitting program", no_titlebar=True, auto_close=True, auto_close_duration=2, font=config["fontSetting"])
    exit(1)
elif not path.exists(saveLocation): # Create a directory for saved files if it doesn't exist already
    mkdir(saveLocation)
savedFiles = Files.get(saveLocation) # Get a list of saved files if there are any


###
# Settings
###
sg.theme("DarkBlue14") # Select theme for the window
fontSetting = "Helvetica 16" # Global font setting for most elements


###
# Run program
###
if __name__ == "__main__": # If program is run directly
    mainWindow.openWindow(savedFiles=savedFiles, config=Files.checkConfig(), saveLocation=config["saveLocation"], fontSetting=config["fontSetting"]) # Open the main window 