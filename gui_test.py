import PySimpleGUI as sg
import json
import util
from threading import Timer
import time

CODES = json.load(open("data/products.json"))
# tuple to have order and set to remove duplicates. sorted to have a consistent order
distinct_names = sorted(tuple(set([CODES[code][1] for code in CODES])))

def calc_price_string(code, count):
    """Calculate the price of a product given its code and count, this is temporary, should be in util
    then return it as a string with nis symbol"""
    
    # price = util.price_calculator(code, count)
    price = round(float(CODES[code][0]) * count, 5) # sometimes floating point errors happen so we round
    return "₪" + str(price)

# functions to be replaced with util
def finish_cart(cart):
    """Finish the cart and print the receipt, this is temporary, should be in util"""
    print("Finished cart:", cart)


def main():
    # Define the layout
    left_layout = [
        [sg.Input("", key="barcode", enable_events=True)],
        [sg.Frame("כמות", [[sg.Button("×"+str(i), key="times-"+str(i)) for i in range(2,11)]], title_location='n')]+
            [sg.Frame("אחר",[[sg.Spin([i for i in range(1000)],key="times_custom"), sg.Button("החל", key="times_custom_ok")]], title_location="n")],
        [sg.Table(  justification="center", values=[], headings=["ברקוד", "פריט", "כמות", "מחיר"], col_widths=[15,10,6,6],
                    auto_size_columns=False, key="cart")],
        [sg.Button("סיום קנייה", key="done", bind_return_key=True), sg.Button("הסר פריט", key="remove")]
    ]
    
    max_width = max([len(name) for name in distinct_names])
    right_col = [
        [sg.Button(name, key="name-"+str(i), size=(max_width,1))]
            for i, name in enumerate(distinct_names)
    ]
    
    layout = [
        [sg.Column(left_layout, element_justification="center"),
        sg.Column(right_col, element_justification="center")]
    ]

    # Create the window
    window = sg.Window("My Window", layout, finalize=True, scaling=4, element_justification="center")
    window.maximize()
    window.bind("<Delete>", "remove")
    window.bind("<Escape>", "reset_cursor")

    # State
    cart = []
    last_barcode_key_time = 0
    def barcode_clear_timer(start_time):
        nonlocal last_barcode_key_time
        if last_barcode_key_time == -1: # the window was closed
            return
        
        if start_time == last_barcode_key_time: # no keys were pressed since the timer started
            window["barcode"].update("")

    # Event loop
    while True:
        event, values = window.read()
        match event:
            case "barcode":
                # clear the barcode after 1 second of no keypresses
                last_barcode_key_time = time.time()
                Timer(1, barcode_clear_timer, [last_barcode_key_time]).start()
                
                # only take numbers
                if len(values["barcode"]) and not values["barcode"][-1].isnumeric():
                    window["barcode"].update(values["barcode"][:-1])

                # this means we're done
                elif values["barcode"] in CODES:
                    cart.append([values["barcode"], CODES[values["barcode"]][1], 1, calc_price_string(values["barcode"], 1)])
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
                cart[-1][3] = calc_price_string(cart[-1][0], count)
            
            case "times_custom_ok":
                if len(cart) == 0:
                    continue
                
                count = int(values["times_custom"])
                cart[-1][2] = count
                cart[-1][3] = calc_price_string(cart[-1][0], count)
            
            case sg.WINDOW_CLOSED:
                break

            case _:
                print("Unknown event:", event, values)

        # Update the cart table in the GUI
        window["cart"].update(cart)
        window["barcode"].set_focus()

    # Close the window
    last_barcode_key_time = -1  # this is to prevent the timer from trying to clear
                                # the barcode after the window is closed
    window.close()


if __name__ == "__main__":
    main()