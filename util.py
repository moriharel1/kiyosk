import json
import time

TIME_OPERATED = time.strftime("%d/%m/%Y/%H:%M:%S") # the time the program operated

DEALS_F = 'data/deals.json'             # en name : [amount, price]
PRICES_F = 'data/prices.json'           # en name : price   
NAMES_F = 'data/name_dictionary.json'   # en name : he name
BARCODES_F = 'data/barcodes.json'       # barcode : en name

PURCHASE_LOG_F = 'data/purchase_log.csv'
COUNT_F = 'data/count.csv'

def read_file(file_name : str):
    """
    read the file and return the data without the first line (the titles in the csv file)

    :param file_name: the file name to read
    :return: the data without the first line
    """

    with open(file_name, 'r') as file:
        data = file.read()
        data = data.split('\n')
        data = [i.split(',') for i in data[1:]]

        return data

def write_file(filename : str, data : list = []):
    """
    write the data to the file and keep what in there until now

    :param filename: the file name to write to
    :param data: the data to write to the file
    """

    with open(filename, 'a') as f:
        for i in data:
            f.write(str(i) + ', ')
        f.write('\n')

with open(PRICES_F, 'r') as f:
    PRICES_DATA = json.load(f)

with open(DEALS_F, 'r') as f:
    DEALS_DATA = json.load(f)
    
with open(NAMES_F, 'r') as f:
    NAMES_DATA = json.load(f)

with open(BARCODES_F, 'r') as f:
    BARCODES_DATA = json.load(f)

PURCHASE_LOG_DATA = read_file(PURCHASE_LOG_F)
COUNT_DATA = read_file(COUNT_F)

COUNT = 0 # count the value of every purchase (the sum of all the purchases)

def load_products():
    """
    load the products to the file from the user input and save it to the file 
    
    :input: barcode, price, name
    """
    while True:
        #check if user wants to continue
        inp = input("press enter to continue or q to quit: ")
        if inp == 'q':
            break

        barcode = input("\nscan product barcode: ")
        price = input("enter product price: ")
        en_name = input("enter product name in english: ")
        he_name = input("enter product name in hebrew: ")

        #update the barcodes file with the new barcode
        data = BARCODES_DATA
        data1 = {barcode : en_name}
        data.update(data1)
        with open(BARCODES_F, 'w') as f:
            json.dump(data, f)

        #update the products file with the new product price
        data = PRICES_DATA
        data1 = {en_name : price}
        data.update(data1)
        with open(PRICES_F, 'w') as f:
            json.dump(data, f)

        #update the names file with the new names of the products in hebrew and english
        data2 = NAMES_DATA
        data3 = {en_name : he_name}
        data2.update(data3)
        with open(NAMES_F, 'w') as f:
            json.dump(data2, f)

def load_deals():
    """
    load the deals to the file from the user input and save it to the file

    :input: barcode, amount, price
    """

    while True:
        #check if user wants to continue
        inp = input("press enter to continue or q to quit: ")
        if inp == 'q':
            break

        barcode = input("\nscan product barcode: ")
        amount = input("enter amount of products in deal: ")
        price = input("enter price of the deal: ")

        #update the deals file with the new deal
        data = DEALS_DATA
        en_name = BARCODES_DATA[barcode]
        data1 = {en_name : [int(amount), float(price)]}
        data.update(data1)
        with open(DEALS_F, 'w') as f:
            json.dump(data, f)

def change_product_price():
    """
    change the price of the product

    :input: barcode, new price
    """

    barcode = input("\nscan product barcode: ")
    new_price = input("enter new price: ")

    #update the products file with the new product price
    data = PRICES_DATA
    en_name = BARCODES_DATA[barcode]
    data1 = {en_name : new_price}
    data.update(data1)
    with open(PRICES_F, 'w') as f:
        json.dump(data, f)

def change_product_he_name():
    """
    change the hebrew name of the product

    :input: barcode, new hebrew name
    """

    barcode = input("\nscan product barcode: ")
    new_he_name = input("enter new hebrew name: ")

    #update the names file with the new hebrew name of the product
    data = NAMES_DATA
    en_name = BARCODES_DATA[barcode]
    data1 = {en_name : new_he_name}
    data.update(data1)
    with open(NAMES_F, 'w') as f:
        json.dump(data, f)

def change_product_en_name():
    """
    change the english name of the product

    :input: barcode, new english name
    """

    barcode = input("\nscan product barcode: ")
    new_en_name = input("enter new english name: ")

    #update the names file with the new english name of the product
    data2 = NAMES_DATA
    data3 = {new_en_name : NAMES_DATA[BARCODES_DATA[barcode]]}
    data2.update(data3)
    with open(NAMES_F, 'w') as f:
        json.dump(data2, f)

    #update the deals file with the new english name of the product
    data4 = DEALS_DATA
    data5 = {new_en_name : DEALS_DATA[BARCODES_DATA[barcode]]}
    data4.update(data5)
    with open(DEALS_F, 'w') as f:
        json.dump(data4, f)

    #update the prices file with the new english name of the product
    data6 = PRICES_DATA
    data7 = {new_en_name : PRICES_DATA[BARCODES_DATA[barcode]]}
    data6.update(data7)
    with open(PRICES_F, 'w') as f:
        json.dump(data6, f)

    #update the barcodes file with the new english name of the product
    data = BARCODES_DATA
    data1 = {barcode : new_en_name}
    data.update(data1)
    with open(BARCODES_F, 'w') as f:
        json.dump(data, f)



def change_product_deal(): 
    """
    change the deal of the product

    :input: barcode, new deal
    """

    barcode = input("\nscan product barcode: ")
    new_amount = input("enter new amount of products in deal: ")
    new_price = input("enter new price of the deal: ")

    #update the deals file with the new deal
    with open(DEALS_F, 'r') as f:
        data = json.load(f)
    en_name = BARCODES_DATA[barcode]
    data1 = {en_name : [int(new_amount), float(new_price)]}
    data.update(data1)
    with open(DEALS_F, 'w') as f:
        json.dump(data, f)

def price_calculator(name: str, amount: int):
    """
    calculate the price of the product

    :param name: the name of the product
    :param amount: the amount of the product to buy
    :return: the price of the products
    """

    #check if the product is in the deals file
    if name in DEALS_DATA:
        #check if the amount is enough for the deal
        if amount >= DEALS_DATA[name][0]:
            #calculate the price
            price = (amount // DEALS_DATA[name][0]) * DEALS_DATA[name][1] + (amount % DEALS_DATA[name][0]) * float(PRICES_DATA[name])
            return price
        
        else: #if the amount that buyed is not enough for the deal
            #calculate the price
            price = amount * float(PRICES_DATA[name])
            return price
            
    else: #if the product is not in the deals file calculate the regular price
        price = amount * float(PRICES_DATA[name])
        return price

def buy(barcode: str, name: str, amount: int = 1, id: str = -1):
    """
    buy the product and update the files

    :param barcode: the barcode of the product
    :param amount: the amount of the product to buy (default is 1)
    """

    if name in PRICES_DATA:
        global COUNT

        price = price_calculator(name, amount)

        #כרגע זה לבדיקה
        print(NAMES_DATA[name] + "price:" + str(price))
        
        #update the count file
        COUNT += float(price)

        #update the purchase log file after all one purchase done
        purchase_log = [str(time.strftime("%d/%m/%Y/%H:%M:%S")), barcode, name, amount, round(price,10), id]
        write_file(PURCHASE_LOG_F, purchase_log)
        return price

    else:
        print("product not found")
        return 0



def main():

    #functions check
    #data = read_file(COUNT_F)                         
    #write_file(COUNT_F, [time, time, count])             
    load_products()  
    load_deals()                                 
    change_product_price()
    change_product_en_name()
    change_product_he_name()
    change_product_deal()

    #buy("1")      
    #print(price_calculator("1",7))

    #
    #every time do this when the program is done
    #time_end_operate = time.strftime("%d/%m/%Y/%H:%M:%S")
    #write_file(COUNT_F, [time_operated, time_end_operate , COUNT])     

    

if __name__ == '__main__':
    main()