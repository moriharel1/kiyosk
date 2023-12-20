import json
import time

TIME_OPERATED = time.strftime("%d/%m/%Y/%H:%M:%S") # the time the program operated

DEALS_F = 'data/deals.json'
PRODUCTS_F = 'data/products.json'
NAMES_F = 'data/name_dictionary.json'
PURCHASE_LOG_F = 'data/purchase_log.csv'
COUNT_F = 'data/count.csv'

def read_file(file_name):
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

def write_file(filename, data : list = []):
    """
    write the data to the file and keep what in there until now

    :param filename: the file name to write to
    :param data: the data to write to the file
    """

    with open(filename, 'a') as f:
        for i in data:
            f.write(str(i) + ', ')
        f.write('\n')

with open(PRODUCTS_F, 'r') as f:
    PRODUCTS_DATA = json.load(f)

with open(DEALS_F, 'r') as f:
    DEALS_DATA = json.load(f)
    
with open(NAMES_F, 'r') as f:
    NAMES_DATA = json.load(f)

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
        he_name = input("enter product name in hebrew: ")
        en_name = input("enter product name in english: ")

        #update the products file with the new product barcode price and the name in hebrew
        with open(PRODUCTS_F, 'r') as f:
            data = json.load(f)
        data1 = {barcode : [price, he_name]}
        data.update(data1)
        with open(PRODUCTS_F, 'w') as f:
            json.dump(data, f)

        #update the names file with the new names of the products in hebrew and english
        with open(NAMES_F, 'r') as f:
            data2 = json.load(f)
        data3 = {he_name : en_name}
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
        with open(DEALS_F, 'r') as f:
            data = json.load(f)
        en_name = NAMES_DATA[PRODUCTS_DATA[barcode][1]]
        data1 = {en_name : [amount, price]}
        data.update(data1)
        with open(DEALS_F, 'w') as f:
            json.dump(data, f)

def price_calculator(barcode, amount):
    """
    calculate the price of the product

    :param barcode: the name of the product
    :param amount: the amount of the product to buy
    :return: the price of the products
    """

    product_name = NAMES_DATA[PRODUCTS_DATA[barcode][1]]

    #check if the product is in the deals file
    if product_name in DEALS_DATA:
        print(DEALS_DATA[product_name])
        print(DEALS_DATA[product_name][0])

        #check if the amount is enough for the deal
        if amount >= DEALS_DATA[product_name][0]:
            #calculate the price
            price = (amount // DEALS_DATA[product_name][0]) * DEALS_DATA[product_name][1] + (amount % DEALS_DATA[product_name][0]) * float(PRODUCTS_DATA[barcode][0])
            return price
        
        else: #if the amount that buyed is not enough for the deal
            #calculate the price
            price = amount * float(PRODUCTS_DATA[barcode][0])
            return price
            
    else: #if the product is not in the deals file calculate the regular price
        price = amount * PRODUCTS_DATA[barcode][0]
        return price

def buy(barcode, amount = 1):
    """
    buy the product and update the files

    :param barcode: the barcode of the product
    :param amount: the amount of the product to buy (default is 1)
    """

    with open(PRODUCTS_F, 'r') as f:
        products = json.load(f)

    if barcode in products:
        global COUNT

        price = price_calculator(products[barcode][1], amount)

        #כרגע זה לבדיקה
        print(products[barcode][1][::-1] + " ריחמ:" + price)
        
        COUNT += float(price)

        #update the purchase log file after all one purchase done
        purchase_log = [str(time.strftime("%d/%m/%Y/%H:%M:%S")), barcode, amount, price, id]
        write_file(PURCHASE_LOG_F, purchase_log)


    else:
        print("product not found")



def main():

    #functions check
    #data = read_file(COUNT_F)                         
    #write_file(COUNT_F, [time, time, count])             
    #load_products()  
    load_deals()                                 
    #buy("1")      
    #print(price_calculator("1",10))

    #
    #every time do this when the program is done
    #time_end_operate = time.strftime("%d/%m/%Y/%H:%M:%S")
    #write_file(COUNT_F, [time_operated, time_end_operate , COUNT])     

    

if __name__ == '__main__':
    main()