
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

        self.gateways: dict[str, BaseGateway] = {}
        self.engines: dict[str, BaseEngine] = {}

    def add_engine(self, engine_class):
        engine = engine_class(self, self.event_engine)
        self.engines[engine.engine_name] = engine
        return engine
    
    # deal with gatewayclass same as engine
    def add_gateway(self, gateway_class):
        gateway = gateway_class(self, self.event_engine)
        self.gateways[gateway.engine_name] = gateway
        return gateway

    def connect(self, gateway_name):
        g = self.gateways[gateway_name]
        if g:
            g.start()
 
