import PySimpleGUI as sg
from Files import Files
import noteWindow


def openWindow(**kwargs):
    searchText = kwargs.get("searchText", "")
    savedFiles = kwargs.get("savedFiles", [])
    config = kwargs.get("config", {})
    saveLocation = kwargs.get("saveLocation", None)
    fontSetting = kwargs.get("fontSetting", "Helvetica 16")

    fontSettings = fontSetting.split() # Splits fontSetting into a list with the font-family and font size as separate items
    fontFamily = fontSettings[0]
    fontSize = fontSettings[1]
    smallerFont = f"{fontFamily} {round(int(fontSize) * 0.75)}"

    static_content = [ # Layout of the buttons and searchbar
        [sg.Text("Saved files", font=fontSetting, justification="center", size=(80, 2))],
        [sg.Button(button_text="Browse", font=smallerFont, key="browse"), sg.Button(button_text="New file", font=smallerFont, key="newFile"), sg.Button(button_text="Refresh", font=smallerFont, key="refresh")],
        [sg.Button("Clear search", font=smallerFont, key="searchClear"), sg.InputText(key="search", default_text=searchText, size=(60,2), enable_events=True), sg.Button("Search", font=smallerFont, key="searchBtn", bind_return_key=True)],
        [sg.Text("", font=fontSetting, justification="center", size=(20, 2))] # Empty row in between the search and saved files
    ]

    dynamic_content = [] # This list will contain all saved files or "No files found"
    if savedFiles: # If savedFiles is not empty
        for i in range(len(savedFiles)):
            if i == 0 or i % 2 == 0:
                if len(savedFiles) > i + 1: # More than 1 file left
                    dynamic_content.append([ # Add a row with these elements in it
                        sg.Text(savedFiles[i], font=fontSetting, justification="center", size=(40, 2), enable_events=True), # Left file
                        sg.Text(savedFiles[i+1], font=fontSetting, justification="center", size=(40, 2), enable_events=True) # Right file
                    ])
                elif len(savedFiles) == i + 1: # Only 1 file left
                    dynamic_content.append([ # Add a row with these elements in it
                        sg.Text(savedFiles[i], font=fontSetting, justification="center", size=(40, 2), enable_events=True) # Centered file
                    ])
    else:
        dynamic_content.append([sg.Text("No files found", font=fontSetting, justification="center", size=(40, 2))])
    
    finalLayout = [[sg.Column(static_content + dynamic_content, element_justification="center", scrollable=True, vertical_scroll_only=True, size=(1000,600))]] # Layout as a column to allow centering elements
    window = sg.Window("Files", layout=finalLayout)

    while True: # Main window event loop
        event, values = window.read() # Read events and values from window
        if event == sg.WIN_CLOSED:
            break # Break out of the loop when the window is closed
        elif event == "browse":
            window.close()
            saveLocation = Files.changeSaveLocation(config)
            openWindow(searchText=values["search"], savedFiles=Files.search(saveLocation=saveLocation), config=config, saveLocation=saveLocation, fontSetting=fontSetting)
        elif event == "searchBtn":
            # values["search"] means whatever text is inside the search bar
            window.close()
            openWindow(searchText=values["search"], savedFiles=Files.search(searchWord=values["search"], config=config, saveLocation=saveLocation), saveLocation=saveLocation)
        elif event == "searchClear":
            window.close()
            openWindow(savedFiles=Files.search(saveLocation=saveLocation), config=config, saveLocation=saveLocation, fontSetting=fontSetting)
        elif event == "newFile":
            newFileName = sg.popup_get_text("Enter a name for the new text file", font=fontSetting, keep_on_top=True)
            if not (newFileName == None or len(newFileName) <= 0):
                Files.new(fileName=newFileName, saveLocation=saveLocation)
        elif event == "refresh":
            window.close()
            openWindow(searchText=values["search"], savedFiles=Files.search(searchWord=values["search"], saveLocation=saveLocation), config=config, saveLocation=saveLocation, fontSetting=fontSetting) # Refresh by reopening window (Files.search returns an updated list of files)
        elif event != "search": # Search event occurs whenever something is being typed in the search bar
            window.close()
            noteWindow.openNote(file=event, savedFiles=savedFiles, config=config, saveLocation=saveLocation, fontSetting=fontSetting) # Event is the name of the clicked file
        
    window.close() # Make sure the window is closed 
