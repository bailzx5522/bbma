
import sys
import requests
import pythonicMT4 
from engine import BaseEngine
from eventEngine import EventEngine, Event
from mainEngine import MainEngine
from gateway import Mt4Gateway

def p(e: Event):
    print(e.data)

def p1(e: Event):
    print(e.data)

class TestEngine(BaseEngine):
    def __init__(self):
        self.engine_name = "TestEngine"
        pass

def main(argv):
    #order_job()
    #trade.remote_subcribe()
    #jobs = []
    #jobs.append(gevent.spawn(sub))
    #jobs.append(gevent.spawn(feed))
    #gevent.joinall(jobs)
    #return

    ee = EventEngine()
    me = MainEngine(ee)
    me.add_gateway(Mt4Gateway)
    me.connect("Mt4Gateway")
    ee.register("test", p)
    ee.register("test", p1)
    #ta = me.add_engine(TestEngine)
    #ee.put(Event("test", "event data"))
    print(123333)
    
if __name__ == "__main__":
    main(sys.argv)