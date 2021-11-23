import PySimpleGUI as sg
from Files import Files
import mainWindow


def openNote(**kwargs):
    file = kwargs.get("file", None)
    savedFiles = kwargs.get("savedFiles", [])
    config = kwargs.get("config", {})
    saveLocation = kwargs.get("saveLocation", None)
    fontSetting = kwargs.get("fontSetting", "Helvetica 16")

    fontSettings = fontSetting.split() # Splits fontSetting into a list with the font-family and font size as separate items
    fontFamily = fontSettings[0]
    fontSize = fontSettings[1]
    smallerFont = f"{fontFamily} {round(int(fontSize) * 0.75)}"

    content = Files.read(file=file, saveLocation=Files.checkConfig()["saveLocation"])
    
    layout = [ # Layout with a text field and save / cancel buttons
        [sg.Text(file, font=fontSetting, justification="center", size=(80, 2))],
        [sg.Button(button_text="Save", font=smallerFont, key="save"), sg.Button(button_text="Exit", font="Helvetica 12", key="exit")],
        [sg.Text("", font=fontSetting, justification="center", size=(20, 2))], # Empty row in between the search and saved files
        [sg.Multiline(default_text=content, font=fontSetting, key="content", size=(100, 25))] # Text field
    ]

    finalLayout = [[sg.Column(layout, element_justification="center", size=(1280,800))]]
    window = sg.Window(file, finalLayout, margins=(None, None), finalize=True)

    window.bind("<Control-s>", "save") # Bind Ctrl + S to "save" event

    while True: # Open file event loop
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break # Break out of the loop when the window is closed
        elif event == "save":
            Files.save(name=file, content=values["content"], saveLocation=saveLocation)
        elif event == "exit":
            window.close()
            mainWindow.openWindow(savedFiles=savedFiles, config=config, saveLocation=saveLocation, fontSetting=fontSetting)
            break
    
    window.close()