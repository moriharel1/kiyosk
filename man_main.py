import util

def main():   
    print("welcome to the kiosk!")
    pas = input("manager password: ")
    if pas == "1234":
        print("welcome manager!")
        what = input("what would you like to do?\n1.add producrs to the kyosk\n2.add deal for the kyosk\n3.exit\nenter your choice: ")
        if what == "1":
            util.add_product()
        elif what == "2":
            util.add_deal()
        elif what == "3":   
            return
        else:
            print("wrong input!")
            main()

    

if __name__ == "__main__":
    main()
