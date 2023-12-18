import PySimpleGUI as sg
import json

CODES = json.load(open("key.json"))

def deal_with_scan(code):
    """deals with a barcode scan, and updates the database

    Args:
        code (str): the barcode scanned (assumes it's in the key.json file)
    """
    global CODES
    
    print(CODES[code])

def main():
    # Define the layout
    layout = [
        [sg.Input("", key="barcode", enable_events=True)],
        [sg.Button("OK")]
    ]

    # Create the window
    window = sg.Window("My Window", layout)

    # Event loop
    while True:
        event, values = window.read()
        print(event, values)
        if event == "barcode":
            if len(values["barcode"]) and not values["barcode"][-1].isnumeric():
                window["barcode"].update(values["barcode"][:-1])

            elif values["barcode"] in CODES:
                deal_with_scan(values["barcode"])
                window["barcode"].update("")
                
        if event == sg.WINDOW_CLOSED or event == "OK":
            break

    # Close the window
    window.close()

if __name__ == "__main__":
    main()