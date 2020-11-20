# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 20:15:31 2018
@author: Ars
"""
import zmq
import numpy as np
class zmq_python():
    
    def __init__(self):
        # Create ZMQ Context
        self.context = zmq.Context()

        # Create REQ Socket
        self.reqSocket = self.context.socket(zmq.REQ)
        self.reqSocket.connect("tcp://localhost:5555")

        # Create PULL Socket
        self.pullSocket = self.context.socket(zmq.PULL)
        self.pullSocket.connect("tcp://localhost:5556")

        #create subcribe Socket
        self.subSocket = self.context.socket(zmq.SUB)
        self.subSocket.connect("tcp://127.0.0.1:6666")

    def remote_sub_recv(self, topic=""):
        try:
            self.subSocket.subscribe(topic)
            top = self.subSocket.recv().decode()
            res = self.subSocket.recv().decode()
            #print("top:",top, "res:", res)
            return top,res
        except Exception as e:
            print("Exception:", e)

    def remote_send(self, socket, data):
    
        try:
            socket.send_string(data)
            msg_send = socket.recv_string()

        except zmq.Again as e:
            print ("Waiting for PUSH from MetaTrader 4..")
            
    def remote_pull(self, socket):
    
        try:
            #msg_pull = socket.recv(flags=zmq.NOBLOCK)
            msg_pull = socket.recv()
            return msg_pull

        except zmq.Again as e:
            print ("Waiting for PUSH from MetaTrader 4..")
            
    
    # return value: [[open...], [high...], [low...], [close...], [datetime...]]
    def get_data(self, symbol, timeframe, start_bar, end_bar, price_type="DATA|"):
        '''
        only start_bar and end_bar as int
        return symbol|open,high,low,close,time|...|...
        '''
        #price_type=DATA|           #history prices
        #self.data = price_type+ symbol+"|"+"PERIOD_"+timeframe+"|"+str(start_bar)+"|"+str(end_bar+1)
        self.data = price_type+ symbol+"|"+timeframe+"|"+str(start_bar)+"|"+str(end_bar+1)
        self.remote_send(self.reqSocket, self.data)
        prices= self.remote_pull(self.pullSocket)
        prices_str= str(prices)
        price_lst= prices_str.split(sep='|')[1:-1]
        open = []
        high = []
        low = []
        close = []
        time = []
        for s in price_lst:
            rates = s.split(",")
            open.append(float(rates[0]))
            high.append(float(rates[1]))
            low.append(float(rates[2]))
            close.append(float(rates[3]))
            time.append(rates[4])
        open.reverse()
        high.reverse()
        low.reverse()
        close.reverse()
        time.reverse()
        price_arr = np.array([open, high, low, close, time])
        #print(price_arr)
        #price_lst= [s.split(",") for s in price_lst]
        #price_lst= price_lst[::-1]
        #price_arr= np.array(price_lst)
        return price_arr
    
    def get_tick(self, symbol):
        self.data = "RATES|" + symbol
        self.remote_send(self.reqSocket, self.data)
        return self.remote_pull(self.pullSocket)

    
    def send_order(self, action, symbol, stop_loss, take_profit, lots=0.01):
        if action == "buy":
            return self.buy_order(symbol, stop_loss, take_profit, lots)
        elif action == "sell":
            return self.sell_order(symbol, stop_loss, take_profit, lots)
        else:
            raise NameError

    def buy_order(self, symbol, stop_loss, take_profit, lots=0.01):
        self.buy= "TRADE|OPEN|0|"+ str(symbol)+"|"+str(stop_loss)+"|"+str(take_profit)+"|"+str(lots)
        self.remote_send(self.reqSocket, self.buy)
        reply= self.remote_pull(self.pullSocket)
        return reply
    
    def sell_order(self, symbol, stop_loss, take_profit, lots=0.01):
        self.buy= "TRADE|OPEN|1|"+ str(symbol)+"|"+str(stop_loss)+"|"+str(take_profit)+"|"+str(lots)
        self.remote_send(self.reqSocket, self.buy)
        reply= self.remote_pull(self.pullSocket)
        return reply
    
    def close_buy_order(self):
        self.close_buy= "TRADE|CLOSE|0"
        self.remote_send(self.reqSocket, self.close_buy)
        reply= self.remote_pull(self.pullSocket)
        return reply
    
    def close_sell_order(self):
        self.close_sell= "TRADE|CLOSE|1"
        self.remote_send(self.reqSocket, self.close_sell)
        reply= self.remote_pull(self.pullSocket)
        return reply

    def close_order(self, ticket):
        self.close= "TRADE|CLOSE|" + str(ticket)
        self.remote_send(self.reqSocket, self.close)
        reply= self.remote_pull(self.pullSocket)
        return reply