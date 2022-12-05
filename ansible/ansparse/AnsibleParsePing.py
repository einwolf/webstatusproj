from ansparse.AnsibleParse import AnsibleParse

class AnsibleParsePing(AnsibleParse):
    def __init__(self, raw_json):
        super.__init__(raw_json)

    def _parse_raw_json(self):
        self.result = "unknown"
    