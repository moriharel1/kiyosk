from pynput.keyboard import Controller
import time
import json
import random

CODES = json.load(open("data/products.json"))

keyboard = Controller()

input("Press enter to start")
while True:
    barcode = random.choice(list(CODES.keys()))
    time.sleep(1)
    for char in barcode:
        keyboard.press(char)
        keyboard.release(char)
        time.sleep(0.015)
    if input("Continue (n for no)? ") == "n":
        break