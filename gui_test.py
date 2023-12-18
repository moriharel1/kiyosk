import PySimpleGUI as sg
import json

# Define the layout
layout = [
    [sg.Input("", key="barcode", enable_events=True)],
    [sg.Button("OK")]
]

# Create the window
codes = json.load(open("key.json"))
window = sg.Window("My Window", layout)

# Event loop
while True:
    event, values = window.read()
    print(event, values)
    if event == "barcode":
        if not values["barcode"][-1].isnumeric():
            window["barcode"].update(values["barcode"][:-1])
        elif values["barcode"] in codes:
            print(codes[values["barcode"]])
            window["barcode"].update("")
    if event == sg.WINDOW_CLOSED or event == "OK":
        break

# Close the window
window.close()
