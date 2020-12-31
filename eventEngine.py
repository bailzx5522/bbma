
from collections import defaultdict 
from threading import Thread
from queue import Queue,Empty

class Event:
    """
    Event object consists of a type string which is used
    by event engine for distributing event, and a data
    object which contains the real data.
    """

    def __init__(self, type: str, data= None):
        """"""
        self.type: str = type
        self.data= data

class EventEngine():
    def __init__(self):
        self.active = False
        self.queue = Queue()
        self.thread = Thread(target=self.run)
        self.timer = Thread(target=self.run_timer)
        self.handlers = defaultdict(list)

    def put(self, event : Event):
        self.queue.put(event)

    def register(self, type_name, handler):
        handler_list = self.handlers[type_name]
        if handler not in handler_list:
            handler_list.append(handler)

    def process(self, event):
        if event.type in self.handlers:
            [handler(event) for handler in self.handlers[event.type]]

    def run(self):
        while self.active:
            try:
                event = self.queue.get(block=True, timeout=1)
                self.process(event)
            except Empty:
                pass

    def run_timer(self):
        pass

    def start(self):
        self.active = True
        self.thread.start()
        #self.timer.start()
