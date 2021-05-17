import websocket, json, pprint, numpy, talib, requests
import push_notification_service

price_target = 0
trade_symbol = "BNBUSDT"
price_state = "HIGHER"


print("Enter trade symbol")
trade_symbol = input("Symbol(default = BNBUSDT): ")
if trade_symbol in ["", " ", None]:
    trade_symbol = 'BNBUSDT' 
while (price_target in ["", " ", None, 0]):
    price_target = float(input("Enter target price here: "))
price_state_choice = input(f"Alert when price is lower(<) than {price_target}(default = Y): ")
if (price_state_choice in ["y", "Y", None, "", " "]):
    price_state = "LOWER"


FUTURES_SOCKET = f"wss://fstream.binance.com/ws/{trade_symbol.lower()}@kline_1m"


def on_open(ws):
    print("Connection opened")

def on_close(ws):
    print("Connection closed")

def on_message(ws, message):
    msg = json.loads(message)

    candle = msg['k']
    is_candle_closed = candle['x']
    close_value = candle['c']

    if is_candle_closed:
        if (price_state == "HIGHER" and float(close_value) > float(price_target)):
            print("should notifiy for higher")
            push_notification_service.send_notification_to_mobile(f"{trade_symbol} price alert", f"{trade_symbol} is at {close_value} above your target of {price_target}")

        if (price_state == "LOWER" and float(close_value) < float(price_target)):
            print("should notifiy for lower")
            push_notification_service.send_notification_to_mobile(f"{trade_symbol} price alert", f"{trade_symbol} is at {close_value} below your target of {price_target}")




ws = websocket.WebSocketApp(FUTURES_SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()
