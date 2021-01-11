
import sys
import requests
import pythonicMT4 
from engine import BaseEngine
from eventEngine import EventEngine, Event, EVENT_TICK
from mainEngine import MainEngine
from gateway import Mt4Gateway

def debug_print(e: Event):
    print(e.data)

class BarGenerator:
    def __init__(self, on_bar_func):
        self.on_bar = on_bar_func

    def update_tick(self):
        pass


class Strategy:
    def __init__(self):
        self.bg = BarGenerator(self.on_bar)

    def on_bar(self):
        pass

    def on_tick(self):
        pass

class MyTestEngine(BaseEngine):
    def __init__(self, main_engine, event_engine):
        self.event_engine = event_engine
        self.main_engine = main_engine
        self.engine_name = "MyTestEngine"

    def init_engine(self):
        self.event_engine.register(EVENT_TICK, self.on_tick_price)

    def on_tick_price(self, event):
        from datetime import datetime
        print("in my test engine\n", datetime.now(), event.data)

    def on_xxx(self, event):
        pass

def main(argv):
    ee = EventEngine()
    me = MainEngine(ee)
    me.add_gateway(Mt4Gateway)
    me.connect("Mt4Gateway")
    #ee.register("tick", debug_print)

    myEngine = me.add_engine(MyTestEngine)
    myEngine.init_engine()

    print("main...")
    
if __name__ == "__main__":
    main(sys.argv)