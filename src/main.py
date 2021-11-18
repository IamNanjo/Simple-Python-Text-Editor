import PySimpleGUI as sg # pip install pysimplegui
from os import listdir, mkdir, path # List directory contents, make directory and path for checking if paths exist
from time import strftime, localtime # Time library 

if not path.exists("./savedNotes"): # Create a directory for saved notes if it doesn't exist already
    mkdir("./savedNotes")

sg.theme("DarkBlue14") # Select theme for the window

fontSetting = "Helvetica 16" # Global font setting for most elements

###
# Functions
###

class Notes: # Contains functions for handling saved notes
    def get(): # Checks all saved notes and returns them as a list    
        return sorted(filter(lambda x: x.endswith(".txt"), listdir("./savedNotes/")), reverse=False) # Filter out all files without .txt file extension
    
    def search(searchWord=""): # Filters notes based on search word(s)
        global savedNotes
        global root

        notes = [note.lower() for note in Notes.get()] # Get a list of saved notes and change all of them to lowercase

        if path.exists("./savedNotes"):
            if len(listdir("./savedNotes/")) > 0:
                savedNotes = sorted(filter(lambda x: searchWord.lower() in x, notes), reverse=False) # Update notes to match search criteria
            else:
                savedNotes = []

    def new(fileName=strftime("%d.%m.%Y_%H.%M.%S", localtime())):
        if fileName + ".txt" in listdir("./savedNotes") and len(listdir("./savedNotes/")) > 0:
            return "File already exists"
        else:
            with open(f"./savedNotes/{fileName}.txt", "x") as f:
                pass

    def read(note):
        try:
            with open(f"./savedNotes/{note}", "r") as f:
                return f.read()
        except Exception as e:
            print(e)

    def save(name, content):
        try:
            with open(f"./savedNotes/{name}", "w+") as f:
                f.write(content)
                print(f.read())
        except Exception as e:
            # Alert the user that saving the file failed and log error to console
            sg.popup(title="Error", custom_text="Saving failed")
            print(e)
        else:
            sg.popup(custom_text="File saved", no_titlebar=True, modal=False, any_key_closes=True, auto_close=True, auto_close_duration=2)

# Get a list of saved notes if there are any
if len(listdir("./savedNotes/")) > 0:
    savedNotes = Notes.get()
else:
    savedNotes = []

###
# Windows
###

def openNote(note):
    content = Notes.read(note)
    
    global fontSetting

    layout = [ # Layout with a text field and save / cancel buttons
        [sg.Text(note, font=fontSetting, justification="center", size=(80, 2))],
        [sg.Button(button_text="Save", font="Helvetica 12", key="save"), sg.Button(button_text="Cancel", font="Helvetica 12", key="cancel")],
        [sg.Text("", font=fontSetting, justification="center", size=(20, 2))], # Empty row in between the search and saved notes
        [sg.Multiline(default_text=content, font=fontSetting, key="content", size=(100, 25))] # Text field
    ]

    finalLayout = [[sg.Column(layout, element_justification="center", size=(1280,800))]]
    window = sg.Window(note, finalLayout, margins=(None, None))

    while True: # Open note event loop
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break # Break out of the loop when the window is closed
        elif event == "save":
            Notes.save(note, values["content"])
        elif event == "cancel":
            window.close()
            mainWindow()
            break
    
    window.close()


###
# Main window
###

dynamic_content = []

def mainWindow(searchText=""):
    global fontSetting
    global dynamic_content
    global fontSetting

    static_content = [ # Layout of the buttons and searchbar
        [sg.Text("Saved notes", font=fontSetting, justification="center", size=(80, 2))],
        [sg.Button(button_text="New file", font="Helvetica 12", key="newFile"), sg.Button(button_text="Refresh", font="Helvetica 12", key="refresh")],
        [sg.Button("Clear search", font="Helvetica 12", key="searchClear"), sg.InputText(key="search", default_text=searchText, size=(60,2), enable_events=True), sg.Button("Search", font="Helvetica 12", key="searchBtn", bind_return_key=True)],
        [sg.Text("", font=fontSetting, justification="center", size=(20, 2))] # Empty row in between the search and saved notes
    ]

    dynamic_content = []
    if len(savedNotes) > 0: # Check if there are any saved notes
        for i in range(len(savedNotes)):
            if i == 0 or i % 2 == 0:
                if len(savedNotes) > i + 1: # More than 1 note left
                    dynamic_content.append([ # Add a row with these elements in it
                        sg.Text(savedNotes[i], font=fontSetting, justification="center", size=(40, 2), enable_events=True), # Left note
                        sg.Text(savedNotes[i+1], font=fontSetting, justification="center", size=(40, 2), enable_events=True) # Right note
                    ])
                elif len(savedNotes) == i + 1: # Only 1 note left
                    dynamic_content.append([ # Add a row with these elements in it
                        sg.Text(savedNotes[i], font=fontSetting, justification="center", size=(40, 2), enable_events=True) # Centered note
                    ])
    else:
        dynamic_content.append([sg.Text("No notes found", font=fontSetting, justification="center", size=(40, 2))])
    
    finalLayout = [[sg.Column(static_content + dynamic_content, element_justification="center", scrollable=True, vertical_scroll_only=True, size=(1000,600))]] # Layout as a column to allow centering elements
    window = sg.Window("Notes", layout=finalLayout)

    while True: # Main window event loop
        event, values = window.read() # Read events and values from window
        if event == sg.WIN_CLOSED:
            break # Break out of the loop when the window is closed
        elif event == "searchBtn":
            Notes.search(values["search"]) # values["search"] means whatever text is inside the search bar
            window.close()
            mainWindow(values["search"])
        elif event == "searchClear":
            Notes.search() # Empty search means clearing the filter
            window.close()
            mainWindow()
        elif event == "newFile":
            newFileName = sg.popup_get_text("Enter a name for the new text file", font=fontSetting, keep_on_top=True)
            if not (newFileName == None or len(newFileName) <= 0):
                Notes.new(newFileName)
        elif event == "refresh":
            window.close()
            mainWindow(values["search"])
        elif event != "search":
            window.close()
            openNote(event) # Event means the clicked note in this case
        
    window.close() # Make sure the window is closed 


if __name__ == "__main__": # If program is run directly
    mainWindow() # Open the main window