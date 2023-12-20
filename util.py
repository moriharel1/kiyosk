import json
import time

TIME_OPERATED = time.strftime("%d/%m/%Y/%H:%M:%S") # the time the program operated

DEALS_F = 'data/deals.json'
PRODUCTS_F = 'data/products.json'
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

PURCHASE_LOG_DATA = read_file(PURCHASE_LOG_F)
COUNT_DATA = read_file(COUNT_F)

COUNT = 0 # count the value of every purchase (the sum of all the purchases)

def load_products():
    """
    load the products to the file from the user input and save it to the file 
    this is manager option

    :input: barcode, price, name
    """
    while True:
        #check if user wants to continue
        inp = input("press enter to continue or q to quit: ")
        if inp == 'q':
            break

        barcode = input("\nscan product barcode: ")
        price = input("enter product price: ")
        name = input("enter product name: ")

        with open(PRODUCTS_F, 'r') as f:
            data = json.load(f)

        data1 = {barcode : [price, name]}
        data.update(data1)
        
        with open(PRODUCTS_F, 'w') as f:
            json.dump(data, f)

def price_calculator(barcode, amount):
    """
    calculate the price of the product

    :param barcode: the name of the product
    :param amount: the amount of the product to buy
    :return: the price of the products
    """

    name_dict = {"\u05d7\u05de\u05e6\u05d5\u05e5" : "hamzoz"}

    product_name = name_dict[PRODUCTS_DATA[barcode][1]]
    print(product_name)

    #check if the product is in the deals file
    if product_name in DEALS_DATA:
        for i in DEALS_DATA[product_name]:
            print(DEALS_DATA[product_name])
            print(DEALS_DATA[product_name][i][0])

            #check if the amount is enough for the deal
            if amount >= DEALS_DATA[product_name][i][0]:
                #calculate the price
                price = (amount // DEALS_DATA[product_name][0]) * DEALS_DATA[product_name][1] + (amount % DEALS_DATA[product_name][0]) * PRODUCTS_DATA[barcode][0]
                return price
            
            else: #if the amount that buyed is not enough for the deal
                #calculate the price
                price = amount * PRODUCTS_DATA[barcode][0]
                return price
            
    else: #if the product is not in the deals file calculate the 
        #calculate the price
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
    #buy("1")      

    #every time do this when the program is done
    #time_end_operate = time.strftime("%d/%m/%Y/%H:%M:%S")
    #write_file(COUNT_F, [time_operated, time_end_operate , COUNT])     

    print(price_calculator("1",1))
    

if __name__ == '__main__':
    main()