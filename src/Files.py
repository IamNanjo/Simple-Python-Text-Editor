import PySimpleGUI as sg
import json
from os import listdir, path

###
# Contains functions for handling files
###

class Files:
    def get(saveLocation=None): # Checks all saved files and returns them as a list    
        if listdir(saveLocation): # Returns true if there are files in saveLocation
            return sorted(listdir(saveLocation)) # Return list of files
        else:
            return []

    def search(**kwargs): # Filters files based on search word(s)
        searchWord = kwargs.get("searchWord", "")
        saveLocation = kwargs.get("saveLocation", None)

        files = [fileName.lower() for fileName in Files.get(saveLocation)] # Get a list of saved files and change all of them to lowercase

        if path.exists(saveLocation) and listdir(saveLocation):
            savedFiles = sorted(filter(lambda x: searchWord.lower() in x, files)) # Update files to match search criteria
        else:
            savedFiles = []
        return savedFiles

    def new(**kwargs): # Creates a new file with given name
        fileName = kwargs.get("fileName", None)
        saveLocation = kwargs.get("saveLocation", None)

        if fileName + ".txt" in listdir(saveLocation) and len(listdir(saveLocation)) > 0:
            return "File already exists"
        else:
            with open(f"{saveLocation}/{fileName}.txt", "x") as f: # Create file with name fileName in saveLocation
                pass

    def read(**kwargs):
        file = kwargs.get("file", None)
        saveLocation = kwargs.get("saveLocation", None)

        try:
            with open(f"{saveLocation}/{file}", "r") as f:
                return f.read()
        except:
            pass
        
    def checkConfig(resetConfig=False):
        config = {}
        if resetConfig:
            try:
                with open(".config.json", "w+") as f:
                    config = {
                        "fontSetting": "Helvetica 16",
                        "saveLocation": "./savedFiles"
                    }
                    json.dump(config, f, indent=2)
            except:
                pass
        else:
            try:
                if path.isfile("./config.json"): # If config.json exists
                    with open("./config.json", "r") as f:
                        config = json.load(f) # Load file as a Python dictionary
                else:
                    with open("./config.json", "w+") as f:
                        config = {
                            "fontSetting": "Helvetica 16",
                            "saveLocation": "./savedFiles"
                        }
                        json.dump(config, f, indent=2)
            except Exception as e:
                print("Failed to load config", e, sep=" | ")
                sg.popup(title="Error", custom_text="Failed to load configuration file. Resetting settings", no_titlebar=True, auto_close=True, auto_close_duration=2, font=config["fontSetting"])
                
        return config

    def changeSaveLocation(config):
        saveLocation = sg.popup_get_folder("Choose directory", default_path=config["saveLocation"]) # Get input from user and set that as the save location
        if not saveLocation: # If user cancels the prompt
            saveLocation = config["saveLocation"]
            return saveLocation # Return the old value
        if saveLocation != config["saveLocation"]: # If saveLocation has been changed
            try:
                with open("./config.json", "w+") as f:
                    config["saveLocation"] = saveLocation
                    json.dump(config, f, indent=2)
            except Exception as e:
                print("Failed to change saveLocation", e, sep=" | ")
        
        return saveLocation

    def save(**kwargs):
        name = kwargs.get("name", None)
        content = kwargs.get("content", None)
        saveLocation = kwargs.get("saveLocation", None)

        try: # Attempt to save file
            with open(f"{saveLocation}/{name}", "w+") as f:
                f.write(content)
        except Exception as e: # Saving failed
            sg.popup(title="Error", custom_text="Saving failed")
            print(e)
        else: # File saved
            sg.popup(custom_text="File saved", no_titlebar=True, modal=False, auto_close=True, auto_close_duration=1)
