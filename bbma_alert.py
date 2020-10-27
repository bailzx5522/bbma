import pythonicMT4 
import talib
import numpy as np
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
    symbol= 'EURUSD'
    symbols = ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "XAUUSD"]
    timeframe= 'H1'
    timeframes= ["M5", "M15", "M30", "H1"]
    start= 0
    end= 200
    ma_period = 5
    stopLoss= 500
    takeProfit= 1000
    order= ''

    while True:
        try:
#vector[-1] is current(not closed) candle
#vector[-2] is previous candle
            prices_close = trade.get_data(symbol= symbol, timeframe= 'M15', start_bar=start, end_bar=end)
            prices_high = trade.get_data(symbol= symbol, timeframe= 'M15', start_bar=start, end_bar=end, price_type="DATA1|")
            prices_low = trade.get_data(symbol= symbol, timeframe= 'M15', start_bar=start, end_bar=end, price_type="DATA2|")
            sma_low = talib.EMA(prices_low, timeperiod=ma_period)
            sma_high = talib.EMA(prices_high, timeperiod=ma_period)
            bbupper, bbmiddle, bblower = talib.BBANDS(prices_close, 20)

            print ("Prev price: {} \nupper: {}\nbblower: {}\nsma_low: {}\n".format(
                prices_close[-2], bbupper[-2], bblower[-2], sma_low[-2], sma_low[-2]))

            for i,val in np.ndenumerate(prices_close):
                print(val, i)
                if sma_high[i] > bbupper[i]:
                    print("over bought")
                elif sma_low[i] < bblower[i]:
                    print("over sold")

            #if order != 'Buy' and order != 'Sell':
            #    if (prices[-1] > prices [-2]) and (prices[-1]<SMA[-1]):
            #        order= 'Buy'

            #    else:
            #        if (prices[-1] < prices[-2]) and (prices[-1] > SMA[-1]):
            #            order= 'Sell'

            #if order== 'Buy' and prices[-1]>SMA[-1]:
            #    order= ''

            #else:
            #    if order== 'Sell' and prices[-1]<SMA[-1]:
            #        order= ''
        except Exception as e:
            print("Error occur", e)
            sleep(3)
            continue
        
        sleep(60)


def main():
    #sma()
    bbma()

if __name__ == "__main__":
    main()