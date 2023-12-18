import json
import time

DEALS_F = 'deals.json'
PRODUCTS_F = 'products.json'
PURCHASE_LOG_F = 'purchase_log.csv'
COUNT_F = 'count.csv'

with open(DEALS_F, 'r') as f:
    DEALS_DATA = json.load(f)

COUNT = 0 # count the value of every purchase (the sum of all the purchases)
time_operated = time.strftime("%d/%m/%Y/%H:%M:%S") # the time the program operated

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

def price_calculator(name, amount):
    """
    calculate the price of the product

    :param barcode: the name of the product
    :param amount: the amount of the product to buy
    :return: the price of the products
    """


    #return price

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
    time_end_operate = time.strftime("%d/%m/%Y/%H:%M:%S")
    write_file(COUNT_F, [time_operated, time_end_operate , COUNT])                
    

if __name__ == '__main__':
    main()