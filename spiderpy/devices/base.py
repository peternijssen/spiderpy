class SpiderDevice(object):
    def __init__(self, data, api):
        self.api = api
        self.data = data

    @property
    def id(self):
        return self.data.get('id')

    @property
    def name(self):
        return self.data.get('name')

    @property
    def model(self):
        return self.data.get('model')

    @property
    def type(self):
        # 105 == Thermostat
        # 103 == PowerPlug
        # 200 == Energy Devices (Also contains PowerPlug)
        return self.data.get('type')

    @property
    def is_online(self):
        return self.data.get('isOnline')
