from ansparse.AnsibleParse import AnsibleParse

class AnsibleParsePing(AnsibleParse):
    def __init__(self, raw_json):
        super().__init__(raw_json)

    def _parse_raw_json(self):
        # get_facts result is first task
        facts_hosts = self.raw_json["plays"][0]["tasks"][0]["hosts"]

        # Ping result is second task
        hosts = self.raw_json["plays"][0]["tasks"][1]["hosts"]

        # Build result
        self.result = {}
        for host in hosts:
            self.result[host] = False
            if hosts[host]["ping"] == "pong":
                self.result[host] = True
    
    def parse_json(self):
        self._parse_raw_json()
