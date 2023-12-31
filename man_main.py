import util

def main():   
    print("welcome to the kiosk!")
    pas = input("manager password: ")
    if pas == "1234":
        print("welcome manager!")
        what = input("what would you like to do?\n1.add producrs to the kyosk\n2.add deal for the kyosk\n3.change product price\n4.change hebrew product name\n5.change english product name\n6.change product deal\n7.delete product by barcode\n8.exit\nenter your choice: ")
        if what == "1":
            util.load_products()
        elif what == "2":
            util.load_deals()
        elif what == "3":
            util.change_product_price()
        elif what == "4":
            util.change_product_he_name()
        elif what == "5":
            util.change_product_en_name()
        elif what == "6":
            util.change_product_deal()
        elif what == "7":
            util.delete_product_by_barcode()
        elif what == "8":
            print("goodbye!")
            return
        else:
            print("wrong input!")
            main()

    
if __name__ == "__main__":
    main()
