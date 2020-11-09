import pythonicMT4 
import talib
import numpy as np
import gevent
import requests
from datetime import datetime
from time import sleep

trade= pythonicMT4.zmq_python()

def sma():
    symbol= 'EURUSD'
    timeframe= 'H1'
    start= 0
    end= 200
    period= 96
    stopLoss= 500
    takeProfit= 1000
    order= ''

    while True:
        try:
            prices= trade.get_data(symbol= symbol, timeframe= 'H1', start_bar=start, end_bar=end)
            SMA= talib.SMA(prices, timeperiod=period)
            print ("Current price: {} \nSMA: {}".format(prices[-1], SMA[-1]))

            if order != 'Buy' and order != 'Sell':
                if (prices[-1] > prices [-2]) and (prices[-1]<SMA[-1]):
                    order= 'Buy'
            #        #trade.buy_order(symbol= symbol, stop_loss= stopLoss, take_profit= takeProfit)

                else:
                    if (prices[-1] < prices[-2]) and (prices[-1] > SMA[-1]):
                        order= 'Sell'
            #            #trade.sell_order(symbol= symbol, stop_loss= stopLoss, take_profit= takeProfit)

            if order== 'Buy' and prices[-1]>SMA[-1]:
                order= ''
            #    #trade.close_buy_order()

            else:
                if order== 'Sell' and prices[-1]<SMA[-1]:
                    order= ''
            #        #trade.close_sell_order()
        except Exception as e:
            print("Error occur", e)
            continue
        
        sleep(3)


def bbma():
    timeframes = [5, 15, 30, 60]
    symbols = ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "XAUUSD"]
    start= 0
    end= 60
    ma_period = 5

#vector[-1] is current(not closed) candle
#vector[-2] is previous candle
    while True:
        minute = datetime.now().minute
        second = datetime.now().second
        if minute % 5 == 0 and second == 0:
            inv = 5
        elif minute % 15 == 0 and second == 0:
            inv = 15
        elif minute % 30 == 0 and second == 0:
            inv = 30
        elif minute % 60 == 0 and second == 0:
            inv = 60
        else:
            gevent.sleep(1)
            continue
        for s in symbols:
            
            prices_close = trade.get_data(symbol= s, timeframe= str(inv), start_bar=start, end_bar=end)
            prices_high = trade.get_data(symbol= s, timeframe= str(inv), start_bar=start, end_bar=end, price_type="DATA1|")
            prices_low = trade.get_data(symbol= s, timeframe= str(inv), start_bar=start, end_bar=end, price_type="DATA2|")
            try:
                ma_low = talib.WMA(prices_low, timeperiod=ma_period)
                ma_high = talib.WMA(prices_high, timeperiod=ma_period)
                ema_50 = talib.EMA(prices_close, timeperiod=50)
                bbupper, bbmiddle, bblower = talib.BBANDS(prices_close, 20)

                print("Syncing", s, inv, "@", datetime.now())
                #print (s, " Prev price: {} \nupper: {}\nbblower: {}\nsma_low: {}\n".format(
                #    prices_close[-2], bbupper[-2], bblower[-2], ma_low[-2], ma_low[-2]))

                #for i,val in np.ndenumerate(prices_close):
                #    if ma_high[i] > bbupper[i]:
                #        print(s,inv, end-i[0],",price:", val ,",hma:", ma_high[i], ",bbupper:", bbupper[i], ",over bought.")
                #    elif ma_low[i] < bblower[i]:
                #        print(s,inv, end-i[0],",price:", val, ",lma:", ma_low[i], ",bblow:", bblower[i], ",over sell.")
            except Exception as e:
                print("Error occur", e)
                sleep(3)
                continue
    
        gevent.sleep(1)

# 5hima>bb
# alert
# make s
# if not making_s and price >= 5highma:

# 5lwma<bb
# alert
# make b
# if making_b and price <= 5lowma:


def feed():
    return

    while True:
        symbols = ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "XAUUSD"]
        for s in symbols:
            rates = trade.get_tick(s)
            print(rates)
        gevent.sleep(1)

# telegram
# api:    https://core.telegram.org/bots/api#sendmessage
def send_alert(message):
    print("Send message:{}".format(message))
    return
    #token:1487299749:AAHb-0rkOo18J4TQ6cuWR1OTGKikX5sGWn4
    bot_token = '1487299749:AAHwGvOysVg4bA3ltzccV68U7EmFJdLp7Mo'
    bot_chatID = '1181612803'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + message

    response = requests.get(send_text)
    json_resp = response.json()
    if json_resp['ok']:
        return
    else:
        print(response.json())


def main():
    gevent.joinall([gevent.spawn(feed),
        gevent.spawn(bbma),
        ])
    

if __name__ == "__main__":
    main()