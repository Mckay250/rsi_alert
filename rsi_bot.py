import websocket, json, pprint, numpy, talib
from notifypy import Notify

SOCKET = "wss://stream.binance.com:9443/ws/egldusdt@kline_1m"



close_values = []

RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = 'EGLDUSDT'

notification = Notify()
notification.audio = "piece-of-cake-611.wav"

def on_open(ws):
    print("Connection opened")

def on_close(ws):
    print("Connection closed")

def on_message(ws, message):
    global close_values
    msg = json.loads(message)

    candle = msg['k']
    is_candle_closed = candle['x']
    close_value = candle['c']

    if is_candle_closed:
        close_values.append(float(close_value))
        print(f"length of close_values {len(close_values)}")
        print(f"1 min candle has closed at {close_value}")

        if len(close_values) > RSI_PERIOD:
            np_closes = numpy.array(close_values)
            rsi = talib.RSI(np_closes, RSI_PERIOD)
            print("all rsis calculated")
            last_rsi = rsi[-1]
            print("current rsi is: ", last_rsi)

            if last_rsi > RSI_OVERBOUGHT:
                print('********** OVERBOUGHT ALERT **********')
                notification.title = TRADE_SYMBOL + " OVERBOUGHT RSI NOTIFICATION"
                notification.message = f"{TRADE_SYMBOL} has been overbought. The RSI unit is at {last_rsi} and the last price is ${close_value}"
                notification.send()
            
            if last_rsi < RSI_OVERSOLD:
                print('********** OVERSOLD ALERT **********')
                notification.title = TRADE_SYMBOL + " OVERSOLD RSI NOTIFICATION"
                notification.message = f"{TRADE_SYMBOL} has been oversold. The RSI unit is at {last_rsi} and the last price is ${close_value}"
                notification.send()











ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()