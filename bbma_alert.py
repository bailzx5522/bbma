import pythonicMT4 
import talib
import numpy as np
import gevent
from gevent import monkey
#monkey.patch_all()
import requests
import sys
import pandas as pd
from datetime import datetime
from time import sleep

# settings
symbols = ["EURUSD"]
tfs = ["15M"]
# Global Data
trade= pythonicMT4.zmq_python()
eu_rates = pd.DataFrame(columns=["date", "bid", "ask"])
gu_rates = pd.DataFrame(columns=["date", "bid", "ask"])
au_rates = pd.DataFrame(columns=["date", "bid", "ask"])
uj_rates = pd.DataFrame(columns=["date", "bid", "ask"])
xau_rates = pd.DataFrame(columns=["date", "bid", "ask"])
 

def send_screenshot():
    pass


class BBMA():
    def __init__(self, sym):
        # parameters/data
        self.sym = sym
        self.prices = None

        # trading conditions
        self.ext = None  #{"action":"buy","ep": "", "ma_ep":bool, }
        self.mhv = None
        #self.reentry = None

        #initialize
        self.init_data()

    def init_data(self):
        self.prices5M = trade.get_data(symbol=self.sym, timeframe= "5M", start_bar=0, end_bar=50, price_type="DATA|")
        self.prices15M = trade.get_data(symbol=self.sym, timeframe= "15M", start_bar=0, end_bar=50, price_type="DATA|")
        self.prices60M = trade.get_data(symbol=self.sym, timeframe= "60M", start_bar=0, end_bar=50, price_type="DATA|")
        #high_prices = np.array(prices_arr[1], dtype="float")
        #hma5 = talib.WMA(high_prices, timeperiod=5)
        #hma10 = talib.WMA(high_prices, timeperiod=10)
        #low_prices = np.array(prices_arr[2], dtype="float")
        #lma10 = talib.WMA(low_prices, timeperiod=10)

    def tick2bar(self):
        # only use bid
        # from tick, we got [o,h,l,c] of 5mins
        self.prices5M = eu_rates["bid"].resample("5Min").ohlc()
        self.prices15M = eu_rates["bid"].resample("15Min").ohlc()
        self.prices60M = eu_rates["bid"].resample("60Min").ohlc()
        #au5M = au_rates["bid"].resample("5Min").ohlc()
        #gu5M = au_rates["bid"].resample("5Min").ohlc()
        #xau5M = au_rates["bid"].resample("5Min").ohlc()
        #uj5M = au_rates["bid"].resample("5Min").ohlc()
        self.eu_rate = eu_rates[["bid", "ask"]].tail(1)
        self.au_rate = au_rates[["bid", "ask"]].tail(1)
        self.gu_rate = gu_rates[["bid", "ask"]].tail(1)
        self.uj_rate = uj_rates[["bid", "ask"]].tail(1)

        #TODO merge new bars to prices_arr
 
    """
    EXTREME:
        uptrend:
            hma5 > bbup
            candle closes in bbup
            reverse candle
            entrypoint: hma5 or zone of high of candle close
            tp: lma5 for safety
        downtrend:
            lma5 < bblow
            ...
        void:
            until candle close out of bbup
        input: array of prices(open high low close)
    """
    def extreme(self):
        WMA_PERIOD = 5
        prices = self.prices["close"]
        prev_close = prices[-2]
        date = prices[4]
        bbup, bbmid, bblow = talib.BBANDS(prices, 20)
        lma5 = talib.WMA(prices_arr[2], timeperiod=WMA_PERIOD)
        hma5 = talib.WMA(prices_arr[1], timeperiod=WMA_PERIOD)
        # check prev candle is EXTREME
        if self.ext is None:
            if hma5[-2] > bbup[-2]:
                self.ext = {"action":"sell", "ep":"{}-{}".format(prices_arr[1][-2]), "ma_ep": True}
            elif lma5[-2] > bblow[-2]:
                self.ext = {"action":"buy", "ep":"{}-{}".format(), "ma_ep": True, "date":date[-2]}
        else:
            #check out previous extreme is invalid.New candle close out of bb(faild)
            if (prev_close > self.ext and prev_close > bbup[-2]) or (prev_close < self.ext and  prev_close < bblow[-2]):
                self.ext = None
                #self.ext_dt = 
        return

    def mhv_perform(self):
        pass

    # reentry after CSM
    # reentry after CSA
    # reentry after CSAK
    # reentry after bigger reentry
    # bb filter(check bbmid for reentry)
    def reentry(self):
        if self.ext and self.mhv:
            #self.pd[]
            #downtrend:retrace to hma5-hma10

            #uptrend:  retrace to lma5-lma10
            return
        else:
            return False
            

    def csa(self):
        pass

    def pattern(self):
        pass

    def run(self):
        new_bar = False
        bbma = BBMA(tf, sym)
        while True:
            if new_bar:
                self.tick2bar()
            self.extreme()

            gevent.sleep(1)

def bbma(symbol, tf):
    start= 0
    end= 60
    ma_period = 5
    last_fetch_time = 0
    #
    upper_ext = 0
    last_upper_ext_time = 0
    lower_ext = 0
    last_lower_ext_time = 0

    while True:
        minute = datetime.now().minute
        fetch_time = datetime.now().timestamp()
        if not(minute % tf == 0 and fetch_time - last_fetch_time > 60):
            gevent.sleep(1)
            continue
        last_fetch_time = fetch_time
        prices_close = trade.get_data(symbol= symbol, timeframe= str(tf), start_bar=start, end_bar=end)
        prices_high = trade.get_data(symbol= symbol, timeframe= str(tf), start_bar=start, end_bar=end, price_type="DATA1|")
        prices_low = trade.get_data(symbol= symbol, timeframe= str(tf), start_bar=start, end_bar=end, price_type="DATA2|")
        try:
            ma_low = talib.WMA(prices_low, timeperiod=ma_period)
            ma_high = talib.WMA(prices_high, timeperiod=ma_period)
            ema_50 = talib.EMA(prices_close, timeperiod=50)
            bbupper, bbmiddle, bblower = talib.BBANDS(prices_close, 20)

            print("Syncing", symbol, tf, "@", datetime.now())
            #print (s, " Prev price: {} \nupper: {}\nbblower: {}\nsma_low: {}\n".format(
            #    prices_close[-2], bbupper[-2], bblower[-2], ma_low[-2], ma_low[-2]))

            # hma > bbupper or lma < bblower
            # close < bblower
            for i,val in np.ndenumerate(prices_close):
                if i == end-1 and ma_high[i] > bbupper[i] and prices_close[-1] < bbupper[i]:
                    upper_ext = prices_high[i]
                    last_upper_ext_time = last_fetch_time
                    msg = "EXTREME\nsymbol:{},tf:{},price:{},hma:{},bbupper:{}".format(symbol, tf, val, ma_high[i], bbupper[i])
                    print(symbol,tf, end-i[0],",price:", val ,",hma:", ma_high[i], ",bbupper:", bbupper[i], ",over bought.")
                    send_alert(msg)
                elif i == end-1 and ma_low[i] < bblower[i] and prices_close[-1] < bblower[i]:
                    lower_ext = prices_low[i]
                    last_lower_ext_time = last_fetch_time
                    msg = "EXTREME\nsymbol:{},tf:{},price:{},lma:{},bblower:{}".format(symbol, tf, val, ma_low[i], bblower[i])
                    print(symbol,tf, end-i[0],",price:", val, ",lma:", ma_low[i], ",bblow:", bblower[i], ",over sell.")
                    send_alert(msg)
        except Exception as e:
            print("Error occur", e)
            sleep(3)
            continue
    
        gevent.sleep(1)

def feed():
    while True:
        print("-------------------------------",datetime.now())
        gevent.sleep(1)

# telegram
# api:    https://core.telegram.org/bots/api#sendmessage
#         https://api.telegram.org/bot<token>/METHOD_NAME
def send_alert(message):
    bot_token = '1487299749:AAHwGvOysVg4bA3ltzccV68U7EmFJdLp7Mo'
    bot_chatID = '1181612803'
    bot_chatID = '-1001229738466'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + message

    response = requests.get(send_text)
    json_resp = response.json()
    if json_resp['ok']:
        return
    else:
        print(response.json())

"""
params:
    sell while price > hma5 @tf
    buy  while price < lma5 @tf
"""
def take_order(action, symbol, lots, tf, close_cond=None):
    sl = 100
    tp = 100
    open = False
    first = True
    ticket = 0
    timeout = tf * 5
    begin = datetime.now().timestamp()
    end = begin + timeout*60
    msg0 = "Ready:{} {} lot:{} TF:M{}\nTimeout:{}".format(action, symbol, lots, tf, end)
    print(msg0)
    #send_alert(msg0)
    while True:
        # use prices_close[-1] instead of bid,ask
        rates = trade.get_tick(symbol).decode()
        bid,ask = rates.split("|")
        #print(bid, ask)
        prices_arr = trade.get_data(symbol=symbol, timeframe= str(tf), start_bar=0, end_bar=30, price_type="DATA|")
        if action == "sell":
            high_prices = np.array(prices_arr[1], dtype="float")
            ma_high = talib.WMA(high_prices, timeperiod=5)
            # if there is no latest data, mt4 may return old data!!!Give 10s to syncing at first time.
            if first:
                first = False
                sleep(10)
                continue
            if float(bid) > float(ma_high[-1]):
                open = True
                price = bid
        elif action == "buy":
            low_prices = np.array(prices_arr[2], dtype="float")
            ma_low = talib.WMA(low_prices, timeperiod=5)
            if first:
                first = False
                gevent.sleep(10)
                continue
            if float(ask) < float(ma_low[-1]):
                open = True
                price = ask

        if open:
            reply = trade.send_order(action, symbol, sl, tp, lots).decode()
            ticket = str(reply).split(",")[1]
            print(reply)
            msg = "reply:{}\n{} {} @{} lot:{} TF:M{}".format(reply, action, symbol, price, lots, tf)
            send_alert(msg)
            break
        else:
            gevent.sleep(1)
            now = datetime.now().timestamp()
            if now > end:
                return
            continue
    if close_cond is None:
        return
    if int(ticket) <= 0:
        print("ticket:",ticket)
        return
    
    close = False
    while True:
        rates = trade.get_tick(symbol).decode()
        bid,ask = rates.split("|")
        #print(bid, ask)
        prices_arr = trade.get_data(symbol=symbol, timeframe= str(tf), start_bar=0, end_bar=30, price_type="DATA|")
        #takeprofit at price < lma5~lma10
        if action == "sell":
            low_prices = np.array(prices_arr[2], dtype="float")
            low_high = talib.WMA(low_prices, timeperiod=5)
            # if there is no latest data, mt4 may return old data!!!Give 10s to syncing at first time.
            if float(ask) < float(low_high[-1]):
                close = True
                price = ask
        #takeprofit at price > hma5~hma10
        elif action == "buy":
            high_prices = np.array(prices_arr[1], dtype="float")
            hma = talib.WMA(high_prices, timeperiod=5)
            if float(bid) > float(hma[-1]):
                close = True
                price = bid
        if close:
            reply = trade.close_order(ticket)
            msg = "close ticket:{},reply:{}\n{}} @{} TF:M{}".format(str(ticket), reply, symbol, price, tf)
            send_alert(msg)
        else:
            gevent.sleep(1)

def order_job():
    jobs = []
    #jobs.append(gevent.spawn(take_order, "sell","EURJPY", 0.5, 60))
    #jobs.append(gevent.spawn(take_order, "buy","EURJPY", 0.5, 60))
    #jobs.append(gevent.spawn(take_order, "sell","AUDUSD", 0.5, 15))
    #jobs.append(gevent.spawn(take_order, "buy","AUDUSD", 0.5, 15))
    #jobs.append(gevent.spawn(take_order, "sell","EURUSD", 0.5, 15))
    #jobs.append(gevent.spawn(take_order, "buy","EURUSD", 0.5, 15))
    #jobs.append(gevent.spawn(take_order, "sell","GBPUSD", 0.5, 5))
    jobs.append(gevent.spawn(take_order, "buy","GBPUSD", 0.5, 15, True))
    #jobs.append(gevent.spawn(take_order, "sell","XAUUSD", 0.5, 5))
    #jobs.append(gevent.spawn(take_order, "buy","XAUUSD", 0.5, 5))
    gevent.joinall(jobs)


def sub():
    temp = {}
    while True:
        sym,rate = trade.remote_sub_recv()
        #print(sym,rate)
        if rate == temp.get(sym):
            continue
        else:
            temp[sym] = rate
            bid,ask = rate.split("|")
            if sym == "EURUSD":
                eu_rate = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d %H:%M:%S"),bid, ask]], columns=["date", "bid", "ask"])
                eu_rates = eu_rates.append(eu_rate)
                print(eu_rates.tail(1))
            elif sym == "GBPUSD":
                gu_rate = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d %H:%M:%S"),bid, ask]], columns=["date", "bid", "ask"])
                gu_rates = gu_rates.append(gu_rate)
            elif sym == "AUDUSD":
                au_rate = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d %H:%M:%S"),bid, ask]], columns=["date", "bid", "ask"])
                au_rates = au_rates.append(au_rate)
            elif sym == "USDJPY":
                uj_rate = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d %H:%M:%S"),bid, ask]], columns=["date", "bid", "ask"])
                uj_rates = uj_rates.append(uj_rate)
            elif sym == "XAUUSD":
                xau_rate = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d %H:%M:%S"),bid, ask]], columns=["date", "bid", "ask"])
                xau_rates = xau_rates.append(xau_rate)
                print(xau_rates.tail(1))
        gevent.sleep(0)


def plotme():
    import matplotlib.pyplot as plt
    f = open("C:\\Users\\dom\\Desktop\\output")
    data = f.readlines()
    result = {}
    for d in data:
        line = d.split(" ")
        ledger = line[0].strip()
        xrp = int(line[1].strip())
        result[ledger] = xrp
    result2 = sorted(result.items(), key=lambda obj: obj[0])
    v = []
    prev = 0
    for r in result2:
        v.append(r[1])
        if prev > 0 and prev - r[1] > 10000000:
            print(r[0], r[1])
        prev = r[1]

    plt.plot(v)
    plt.show(block=True)

def main(argv):
    plotme()
    return
    #order_job()
    #trade.remote_subcribe()
    #jobs = []
    #jobs.append(gevent.spawn(sub))
    #jobs.append(gevent.spawn(feed))
    #gevent.joinall(jobs)
    return
    
if __name__ == "__main__":
    main(sys.argv)