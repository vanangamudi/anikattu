import logging
from pprint import pprint, pformat

logging.basicConfig(format="%(levelname)-8s:%(filename)s.%(funcName)20s >>   %(message)s")
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

class Configurable:
    def __init__(self, config):
        self.config = config
        
class Experiment:
    
