import json
import time

KEY_FILE = r'C:\Users\morih\OneDrive\מסמכים\הראל\תכנות\python\stam_dvarim_py\kiyosk\key.json'
BUYED_PRODUCTS = r'C:\Users\morih\OneDrive\מסמכים\הראל\תכנות\python\stam_dvarim_py\kiyosk\buyed.txt'
COUNT_FILE = r'C:\Users\morih\OneDrive\מסמכים\הראל\תכנות\python\stam_dvarim_py\kiyosk\count.txt'

def load_products():
    while True:
        barcode = input("\nscan product barcode: ")
        price = input("enter product price: ")
        name = input("enter product name: ")


        with open(KEY_FILE, 'r') as f:
            data = json.load(f)

        data1 = {barcode : [price, name]}
        data.update(data1)
        
        with open(KEY_FILE, 'w') as f:
            json.dump(data, f)


        #check if user wants to continue
        inp = input("press enter to continue or q to quit: ")
        if inp == 'q':
            break

count_money = 0 #כמות הכסף שאמורה להיות בקופה מאז שהופעלה התוכנה.סכום של כל הקניות שבוצעו

def buy():
    global count_money
    while True:
        barcode = input("")

        if barcode == 'q': #add the count to the file
            with open(COUNT_FILE, 'r') as files:
                count_to_today = str(files.read())

            count_this_day = str(count_money) + " " + str(time.strftime("%d/%m/%Y/%H:%M:%S")) + "\n"
            count_this_day += count_to_today

            with open(COUNT_FILE, 'w') as files:
                files.write(str(count_this_day))
            break

        with open(KEY_FILE, 'r') as f:
            data = json.load(f)

        if barcode in data:
            with open(BUYED_PRODUCTS, 'r') as file:
                old_data = file.read()

            with open(BUYED_PRODUCTS, 'w') as file:
                file.write(old_data + data[barcode][1][::-1] + " " + data[barcode][0] + " " + str(time.strftime("%d/%m/%Y/%H:%M:%S")) + "\n")
            
            print(data[barcode][1] + " ריחמ:" + data[barcode][0])
            count_money += float(data[barcode][0])


def main():   
    print("welcome to the kiosk!")
    print("what do you want to do?")
    print("1. sell products")
    print("2. exit program")

    user_input = input("enter your choice: ")
    if user_input == '1':
        print("scan products barcode's and after scan press enter")
        buy()
        
    elif user_input == '2':
        return
    
    elif user_input == '1516': #manager mode
        print("manager mode")
        manager_input = input("1. load products, 2. print the money count up to this day \nenter your choice:")
        if manager_input == '1':
            load_products()

        elif manager_input == '2':
            with open(COUNT_FILE, 'r') as files:
                count_to_today = str(files.read())
            print(count_to_today)
        
    else:
        print("invalid input")
        main()

if __name__ == "__main__":
    main()
