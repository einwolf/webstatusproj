from abc import ABC, abstractmethod

class AnsibleParse(ABC):
    def __init__(self, raw_json):
        self.raw_json = raw_json
        self.result = None
    
    @abstractmethod
    def parse_json(self):
        """
        Convert raw_json to result
        """
        self.result = None

    @abstractmethod
    def parse_json(self, host):
        """
        Return parsed result for host
        """
        return self.result[host]