import PySimpleGUIWx as sg
import json

CODES = json.load(open("data/products.json"))

# functions to be replaced with util
def calc_price(code, count):
    """Calculate the price of a product given its code and count, this is temporary, should be in util"""
    global CODES
    
    print("Scanned:", code, "which is", CODES[code])
    return float(CODES[code][0]) * count

def finish_cart(cart):
    """Finish the cart and print the receipt, this is temporary, should be in util"""
    print("Finished cart:", cart)


def main():
    # Define the layout
    layout = [
        [sg.Input("", key="barcode", enable_events=True)],
        [sg.Frame("כמות", [[sg.Button("×"+str(i), key="times-"+str(i)) for i in range(2,11)]], title_location='n')]+
            [sg.Frame("אחר",[[sg.Spin([i for i in range(1000)],key="times_custom"), sg.Button("החל", key="times_custom_ok")]], title_location="n")],
        [sg.Table(justification="right", values=[], headings=["ברקוד", "פריט", "כמות", "מחיר שקלים"], key="cart")],
        [sg.Button("סיום קנייה", key="done", bind_return_key=True), sg.Button("הסר פריט", key="remove")]
    ]

    # Create the window
    window = sg.Window("My Window", layout, finalize=True, scaling=4, element_justification="center")
    window.maximize()
    window.bind("<Delete>", "remove")
    window.bind("<Escape>", "reset_cursor")

    # State
    cart = []

    # Event loop
    while True:
        event, values = window.read()
        match event:
            case "barcode":
                if len(values["barcode"]) and not values["barcode"][-1].isnumeric():
                    window["barcode"].update(values["barcode"][:-1])

                elif values["barcode"] in CODES:
                    cart.append([values["barcode"], CODES[values["barcode"]][1], 1, format(calc_price(values["barcode"], 1),".2f")])
                    window["barcode"].update("")
            
            case "remove":
                to_remove = values['cart']
                for index in sorted(to_remove, reverse=True):
                    del cart[index]
            
            case "done":
                finish_cart(cart)
                cart = []
            
            case "cursor_reset":
                # it's recognized but it's delt with because it's an event 
                pass
            
            case s if type(s) is str and s.startswith("times-"):
                if len(cart) == 0:
                    continue
                
                count = int(event.split("-")[1])
                cart[-1][2] = count
                cart[-1][3] = format(calc_price(cart[-1][0], count), ".2f")
            
            case "times_custom_ok":
                if len(cart) == 0:
                    continue
                
                count = int(values["times_custom"])
                cart[-1][2] = count
                cart[-1][3] = format(calc_price(cart[-1][0], count), ".2f")
            
            case sg.WINDOW_CLOSED:
                break

            case _:
                print("Unknown event:", event, values)

        # Update the cart table in the GUI
        window["cart"].update(cart)
        window["barcode"].set_focus()

    # Close the window
    window.close()

if __name__ == "__main__":
    main()