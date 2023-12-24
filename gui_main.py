import PySimpleGUI as sg
import json
import util
from threading import Timer
import time
import uuid

PRICES = json.load(open("data/prices.json"))              # name: price
DISTINCT_NAMES = list(PRICES.keys())
BARCODES = json.load(open("data/barcodes.json"))            # barcode: name
LANGUAGE_DICT = json.load(open("data/name_dictionary.json"))# english name: hebrew name

def calc_price_string(name, count):
    """Calculate the price of a product given its name and count, this is temporary, should be in util
    then return it as a string with nis symbol"""
    
    price = round(util.price_calculator(name, count), 10)
    return "₪" + str(price)

def collapse_cart(cart):
    """
    group the cart by name, and sum the count and price of each group. it will pick first barcode if any are provided.
    (not that it really matters that much)

    Args:
        cart (list of lists): the cart, each element is [barcode, english name, hebrew name, count, price]
    
    Returns:
        list of lists: the collapsed cart, each element is [barcode, english name, hebrew name, count, price]
    """
    
    collapsed_cart = []
    for barcode, name, hebrew_name, count, price in cart:
        for i, (collapsed_barcode, collapsed_name, collapsed_hebrew_name, collapsed_count, collapsed_price) in enumerate(collapsed_cart):
            if collapsed_name == name:
                collapsed_cart[i][3] += count
                collapsed_cart[i][4] = calc_price_string(name, collapsed_cart[i][3])
                
                if collapsed_cart[i][0] == "" and barcode != "":
                    collapsed_cart[i][0] = barcode
                
                break
        else:
            collapsed_cart.append([barcode, name, hebrew_name, count, price])
    
    return collapsed_cart


# functions to be replaced with util
def finish_cart(cart):
    """Finish the cart and print the receipt, this is temporary, should be in util"""
    final_price = 0
    purchase_id = uuid.uuid4().hex
    for barcode, name, hebrew_name, count, price in cart:
        final_price += util.buy(barcode, name, count, purchase_id)
    
    return final_price


def main():
    # Define the layout
    left_layout = [
        [sg.Input("", key="barcode", enable_events=True)],
        [sg.Frame("כמות", [[sg.Button("×"+str(i), key="times-"+str(i)) for i in range(1,11)]], title_location='n')]+
            [sg.Frame("אחר",[[sg.Spin([i for i in range(1000)],key="times_custom"), sg.Button("החל", key="times_custom_ok")]], title_location="n")],
        [sg.Table(  justification="center", values=[], headings=["ברקוד", "name", "פריט", "כמות", "מחיר"], col_widths=[15,0,14,6,6],
                    auto_size_columns=False, visible_column_map=[True,False,True,True,True], key="cart")], # don't include the english name column
        [sg.Button("סיום קנייה", key="done", bind_return_key=True), sg.Button("הסר פריט", key="remove"), sg.Button("אפס קניה", key="clear"), sg.Text("", key="total")]
    ]
    
    max_width = max([len(LANGUAGE_DICT[name]) for name in DISTINCT_NAMES])
    right_col = [
        [sg.Button(LANGUAGE_DICT[name], key="product-"+str(i), size=(max_width,1))]
            for i, name in enumerate(DISTINCT_NAMES)
    ]

    layout = [
        [sg.Column(left_layout, element_justification="center"),
            sg.Column([[sg.Frame("הוסף סוג", right_col, title_location="n")]],
                        element_justification="center", vertical_alignment="top")],
    ]

    # Determine scaling factor
    root = sg.tk.Tk()
    # this takes the height of the screen, divides by the dpi, and multiplies by constant to have the
    # scale be proportional to screen's scale. so it works for any screen at any dpi
    scaling = root.winfo_screenmmheight() / root.winfo_fpixels('1i') * 1.75
    root.destroy()

    # Create the window
    window = sg.Window("My Window", layout, finalize=True, scaling=scaling, element_justification="right")
    window.maximize()
    window.bind("<Delete>", "remove")
    window.bind("<Escape>", "reset_cursor")

    # State
    cart = [] # list of [barcode, english name, hebrew name, count, price]
    last_barcode_key_time = 0
    
    # helper function for clearing the barcode after 1 second of no keypresses
    def barcode_clear_timer(start_time, cur_value):
        nonlocal last_barcode_key_time
        if last_barcode_key_time == -1: # the window was closed
            return
        
        if start_time == last_barcode_key_time: # no keys were pressed since the timer started
            window["barcode"].update("")
            if len(cur_value) == 1 and cur_value.isnumeric():
                if cur_value == '0': # 0 key used for 10
                    cur_value = '10'
                window.write_event_value("times-"+cur_value, None)

    # Event loop
    while True:
        event, values = window.read()
        match event:
            case "barcode":
                # clear the barcode after 1 second of no keypresses
                last_barcode_key_time = time.time()
                Timer(0.5, barcode_clear_timer, [last_barcode_key_time, values["barcode"]]).start()
                
                # only take numbers
                if len(values["barcode"]) and not values["barcode"][-1].isnumeric():
                    window["barcode"].update(values["barcode"][:-1])

                # this means we're done
                elif values["barcode"] in BARCODES:
                    name = BARCODES[values["barcode"]]
                    cart.append([values["barcode"], name, LANGUAGE_DICT[name], 1, calc_price_string(name, 1)])
                    cart = collapse_cart(cart)
                    window["barcode"].update("")
            
            case "remove":
                to_remove = values['cart']
                for index in sorted(to_remove, reverse=True):
                    del cart[index]
            
            case "clear":
                cart = []
            
            case "done":
                finish_cart(cart)
                cart = []
            
            case "cursor_reset":
                # it's recognized but it's delt with because it's an event 
                pass
            
            case "times_custom_ok":
                count = int(values["times_custom"])
                if len(cart) == 0:
                    continue
                
                positions = [-1]
                if len(values['cart']) != 0:
                    positions = values['cart']
                
                for position in positions:
                    cart[position][3] = count
                    cart[position][4] = calc_price_string(cart[position][1], count)

            
            case s if type(s) is str and s.startswith("times-"):
                count = int(event.split("-")[1])
                if len(cart) == 0:
                    continue
                
                positions = [-1]
                if len(values['cart']) != 0:
                    positions = values['cart']
                
                for position in positions:
                    cart[position][3] = count
                    cart[position][4] = calc_price_string(cart[position][1], count)
            
            case s if type(s) is str and (s.startswith("product-") or s.isnumeric()):
                index = int(s.split("-")[-1])
                name = DISTINCT_NAMES[index]

                cart.append(["", name, LANGUAGE_DICT[name], 1, calc_price_string(name, 1)])
                cart = collapse_cart(cart)
            
            
            case sg.WINDOW_CLOSED:
                break
            
            case _:
                print("Unknown event:", event, values)

        # Update the cart table in the GUI
        window["cart"].update(reversed(cart))
        window["barcode"].set_focus()
        if cart != []:
            total = 0
            for item in cart:
                total += util.price_calculator(item[1], item[3])
            window["total"].update("סה\"כ: ₪" + str(total))

    # Close the window
    last_barcode_key_time = -1  # this is to prevent the timer from trying to clear
                                # the barcode after the window is closed
    window.close()


if __name__ == "__main__":
    main()
    # store info about session
    time_end_operate = time.strftime("%d/%m/%Y/%H:%M:%S")
    util.write_file(util.COUNT_F, [util.TIME_OPERATED, time_end_operate , util.COUNT])
