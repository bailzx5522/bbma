import zmq
import threading
from time import sleep
from eventEngine import Event
from eventEngine import EVENT_TICK
from datetime import datetime

setting = {"req_address":"tcp://127.0.0.1:5555",
           "sub_address":"tcp://127.0.0.1:6666"}


class BaseGateway():
    def __init__(self):
        pass


class Mt4Gateway(BaseGateway):
    def __init__(self, main_engine, event_engine):
        self.engine_name = "Mt4Gateway"
        self.event_engine = event_engine
        self.main_engine = main_engine
        self.active = False

        self.callbacks: Dict[str, Callable] = {
            #"account": self.on_account_info,
            "price": self.on_price_info,
            #"order": self.on_order_info,
            #"position": self.on_position_info,
        }
    def on_price_info(self, packet:dict) -> None:
        if "data" not in packet:
            return
        for d in packet["data"]:
            tick = {"symbol": d["symbol"],
                    "bid":d["bid"],
                    "ask":d["ask"],
                    "datetime":datetime.now()
                    }
            self.on_event(EVENT_TICK, tick)

    def on_event(self, e_type:str, e_data):
        event = Event(e_type, e_data)
        self.event_engine.put(event)

    def start(self):
        self.context: zmq.Context = zmq.Context()
        self.socket_req: zmq.Socket = self.context.socket(zmq.REQ)
        self.socket_pull: zmq.Socket = self.context.socket(zmq.PULL)
        self.socket_sub: zmq.Socket = self.context.socket(zmq.SUB)
        self.socket_sub.setsockopt_string(zmq.SUBSCRIBE, "")
        self.socket_req.connect(setting["req_address"])
        self.socket_sub.connect(setting["sub_address"])

        self.active = True
        self.thread = threading.Thread(target=self.run)
        self.thread.start()
    
    def callback(self, packet):
        callback_function = self.callbacks.get(packet["type"], None)
        if callback_function:
            callback_function(packet)

    def run(self):
        while self.active:
            if not self.socket_sub.poll(1000):
                continue

            #use json
            data = self.socket_sub.recv_json(flags=zmq.NOBLOCK)
            #data = self.socket_sub.recv().decode()
            #print("res:", data)
            self.callback(data)
        self.socket_req.close()
        self.socket_sub.close()