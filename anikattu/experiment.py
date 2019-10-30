import logging
from pprint import pprint, pformat

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


from anikattu.keyedlist import KeyedList

class Configurable:
    def __init__(self, config):
        self.C = KeyedList(config)
        
class Experiment(Configurable):
    def __init__(self, config, model, dataset):
        super().__init__(config)
        self.model = model
        self.dataset = dataset

    def run(self):
        self.model.do_train()
