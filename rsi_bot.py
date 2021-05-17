import websocket, json, pprint, numpy, talib, requests
# from notifypy import Notify
import push_notification_service
import sys

# Get user's inputs
print("Enter trade symbol")

trade_symbol = sys.argv[1]
over_bought = sys.argv[2]
rsi_period = int(sys.argv[3])
rsi_time_frame = int(sys.argv[4])




# trade_symbol = input("Symbol(default = EGLDUSDT): ")
# over_bought = input("Do you want to be Alerted when there is an overbought signal?(Y/N, default = N): ")
# rsi_period = int(input("Enter RSI PERIOD here (default = 7): "))
# rsi_time_frame = int(input("Enter RSI TIME FRAME here (default=15): "))

over_bought_alert = False

if (over_bought in ["Y", "y"]): 
    over_bought_alert = True

if (rsi_period in ["", " ", None]):
    rsi_period = 7

if trade_symbol in ["", " ", None]:
    trade_symbol = 'EGLDUSDT' 
else: 
    TRADE_SYMBOL = trade_symbol

if (rsi_time_frame in ["", " ", None]):
    rsi_time_frame = 15
    

close_values = []

RSI_PERIOD = rsi_period
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = trade_symbol



# notification = Notify()
# notification.audio = "piece-of-cake-611.wav"


SOCKET = f"wss://stream.binance.com:9443/ws/{TRADE_SYMBOL.lower()}@kline_{rsi_time_frame}m"
FUTURES_SOCKET = f"wss://fstream.binance.com/ws/{TRADE_SYMBOL.lower()}@kline_{rsi_time_frame}m"

# PAST_DATA_URL = f"https://fapi.binance.com/fapi/v1/continuousKlines?symbol={TRADE_SYMBOL.upper()}&limit=20&interval={rsi_time_frame}m"
PAST_DATA_URL = f"https://fapi.binance.com/fapi/v1/klines?symbol={TRADE_SYMBOL.lower()}&limit=20&interval={rsi_time_frame}m"

def on_open(ws):
    print("Connection opened")

def on_close(ws):
    print("Connection closed")

def on_message(ws, message):
    global close_values
    msg = json.loads(message)

    candle = msg['k']
    # print("msg is ", msg)
    # print("candle is ", candle)
    is_candle_closed = candle['x']
    close_value = candle['c']

    if is_candle_closed:
        close_values.append(float(close_value))
        print(f"length of close_values {len(close_values)}")
        print(f"{rsi_time_frame} min candle has closed at {close_value}")

        if len(close_values) > RSI_PERIOD:
            title = ""
            message = ""
            np_closes = numpy.array(close_values)
            rsi = talib.RSI(np_closes, RSI_PERIOD)
            print("all rsis calculated")
            last_rsi = rsi[-1]
            print("current rsi is: ", last_rsi)

            if last_rsi > RSI_OVERBOUGHT:
                print('********** OVERBOUGHT ALERT **********')
                if (over_bought_alert):
                    title = TRADE_SYMBOL + " OVERBOUGHT RSI NOTIFICATION"
                    message = f"{TRADE_SYMBOL} has been overbought. The RSI unit is at {last_rsi} and the last price is $ {close_value}"
                    push_notification_service.send_notification_to_mobile(title, message)
                    
            if last_rsi < RSI_OVERSOLD:
                print('********** OVERSOLD ALERT **********')
                title = TRADE_SYMBOL + " OVERSOLD RSI NOTIFICATION"
                message = f"{TRADE_SYMBOL} has been oversold. The RSI unit is at {last_rsi} and the last price is $ {close_value}"
                push_notification_service.send_notification_to_mobile(title, message)





past_data = requests.get(PAST_DATA_URL)
parsed_past_data = past_data.json()
# print(parsed_past_data)
for item in parsed_past_data:
    if (parsed_past_data[-1][0] == item[0]):
        continue
    close_values.append(float(item[4]))
# print("length of close values is: ", len(close_values))
# print(close_values)




ws = websocket.WebSocketApp(FUTURES_SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()