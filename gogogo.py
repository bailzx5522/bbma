
import sys
import requests
import pythonicMT4 
from engine import BaseEngine
from eventEngine import EventEngine, Event, EVENT_TICK
from mainEngine import MainEngine
from gateway import Mt4Gateway, TickData, BarData

def debug_print(e: Event):
    print(e.data)

MIN = "min"
HOUR = "hour"
# funcflow
# testEngine.on_tick() -> strategy.on_tick() -> barGenerator.on_tick() -> strategy.on_bar()
class BarGenerator:
    def __init__(self, on_bar_func, bar_inv=MIN, bar_inv_count=15):
        self.bar : BarData = None
        self.on_bar = on_bar_func

        self.bar_inv = bar_inv
        self.bar_inv_count = bar_inv_count

        self.last_tick : TickData = None

    def update_tick(self, tick : TickData):
        new_minute = False
        
        if self.last_tick and self.last_tick.datetime > tick.datetime:
            return

        if not self.bar:
            new_minute = True
        elif (self.bar.datetime.minute != tick.datetime.minute) or (self.bar.datetime.hour != tick.datetime.hour):
            print("update old bar...")
            self.on_bar(self.bar)
            new_minute = True
        if new_minute:
            self.bar = BarData(symbol=tick.symbol,
            interval = self.bar_inv,
            datetime = tick.datetime,
            open = tick.ask,
            high = tick.ask,
            low = tick.ask,
            close = tick.ask
            )
        else:
            self.bar.high = max(self.bar.high, tick.ask)
            if tick.high > self.last_tick.high:
                self.bar.high = max(self.bar.high, tick.high)

            self.bar.low = min(self.bar.low, tick.last)
            if tick.low < self.last_tick.low:
                self.bar.low = min(self.bar.low, tick.low)

            self.bar.close = tick.ask
            self.bar.datetime = tick.datetime



    def update_bar(self, bar):
        pass

class MyStrategy:
    def __init__(self):
        self.bg = BarGenerator(self.on_bar)

    def on_bar(self):
        pass

    def on_tick(self, tick : TickData):
        print("in myStrategy engine\n", tick.symbol, tick.bid)
        self.bg.update_tick(tick)

class MyTestEngine(BaseEngine):
    def __init__(self, main_engine, event_engine):
        self.event_engine = event_engine
        self.main_engine = main_engine
        self.engine_name = "MyTestEngine"
        self.bg = BarGenerator(self.on_bar)
        self.strategy = {MyStrategy()}

    def on_init(self):
        #load history bar for indicators
        pass

    def init_engine(self):
        self.event_engine.register(EVENT_TICK, self.on_tick_price)

    def on_tick_price(self, event):
        #from datetime import datetime
        #print("in my test engine\n", datetime.now(), event.data)
        for s in self.strategy:
            s.on_tick(event.data)

    def on_bar(self, event):
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
    #test()