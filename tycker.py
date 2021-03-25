#!/usr/bin/env python
import config as cfg
import websocket
import json
from os import system, name
from termcolor import colored
from pyfiglet import figlet_format

last_price = -1.0
ticker = ''


def on_message(ws, message):
    try:
        message = json.loads(message)
        price = float(message['data'][0]['p'])
        clear()
        global last_price
        global ticker
        if price < last_price:
            print(colored(figlet_format(ticker + '\t' +
                  price, justify="center"), color="red"))
        else:
            print(colored(figlet_format(price), color="green"))
        last_price = price
    except:
        pass


def on_error(ws, error):
    print(error)
    exit()


def on_open(ws):
    global ticker
    ws.send('{"type":"subscribe","symbol":"'+ticker+'"}')


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def main():
    global ticker
    ticker = input("Ticker: ")
    key = cfg.keys["finnhub"]
    system('setterm -cursor off')
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=" + key,
                                on_message=on_message,
                                on_error=on_error)
    ws.on_open = on_open
    ws.run_forever()


if __name__ == "__main__":
    main()
