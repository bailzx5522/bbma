
from gateway import BaseGateway
from eventEngine import EventEngine
from engine import BaseEngine

class MainEngine():
    def __init__(self, event_engine:EventEngine=None):
        if event_engine:
            self.event_engine = event_engine
        else:
            self.event_engine = EventEngine()
        self.event_engine.start()

        self.gateway: dict[str, BaseGateway] = {}
        self.engines: dict[str, BaseEngine] = {}

    def add_engine(self, engine_class):
        engine = engine_class(self, self.event_engine)
        self.engines[engine.engine_name] = engine
        return engine
    
    def add_gateway(self, gateway_calss):
        gw = gateway_class(self, self.event_engine)
        self.engines[engine.engine_name] = engine
        return engine
 
