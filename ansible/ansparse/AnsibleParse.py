from abc import ABC, abstractmethod

class AnsibleParse(ABC):
    def __init__(self, raw_json):
        self.raw_json = raw_json
        self.result = None

    @abstractmethod
    def _parse_raw_json(self):
        pass
    