
class Analytics:
    def __init__(self, timestamp: str = None, url: str = None,event : dict=None):
        self.timestamp = timestamp
        self.url = url
        self.event = event

    def to_dict(self):
        analytics_dict = {}
        analytics_dict['timestamp'] = self.timestamp
        analytics_dict['url'] = self.url
        analytics_dict['event'] = self.event
        return analytics_dict
