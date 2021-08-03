import PySimpleGUI as sg
import os.path
import buttonEvents


file_list_column = [
    [
        sg.Text("Image Folder"),
        sg.In(size=(25, 1), enable_events=True, key="-IMGFOLDER-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Text("Annotations"),
        sg.In(size=(25, 1), enable_events=True, key="-CSVFILE-"),
        sg.FileBrowse(),
    ]]
layout = [
    [
        [sg.Column(file_list_column)],
        [sg.Text(size=(40, 1), key="-TOUT-")],
        [sg.Button('Predict')], 
        [sg.Button('Send to DB')],
        [sg.Button('Retraining')]
    ]]

window = sg.Window("Auto WSP", layout, element_justification='center')

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    if event == "-IMGFOLDER-":
        folder = values["-IMGFOLDER-"]
        try:
        # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []
    elif event == 'Predict':
        predictions_path = buttonEvents.predict(values["-IMGFOLDER-"])
        window["-TOUT-"].update("Predictions Path: " + predictions_path)
        buttonEvents.my_popup(window)
    elif event == 'Send to DB':
        database_path = buttonEvents.sendToDB(values["-IMGFOLDER-"],values["-CSVFILE-"])
        window["-TOUT-"].update("Database Path: " + database_path)
    elif event == 'Retraining':
        window["-TOUT-"].update("Execute training.pynb")

window.close()
