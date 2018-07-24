from spiderpy.devices.base import SpiderDevice


# noinspection SpellCheckingInspection
class SpiderThermostat(SpiderDevice):

    @property
    def operation_mode(self):
        for prop in self.data.get('properties'):
            if prop['id'] == 'OperationMode':
                return prop['status']

        return "Idle"

    @property
    def has_operation_mode(self):
        for prop in self.data.get('properties'):
            if prop['id'] == 'OperationMode':
                return True

        return False

    @property
    def current_temperature(self):
        for prop in self.data.get('properties'):
            if prop['id'] == 'AmbientTemperature':
                return float(prop['status'])

        return 0.0

    @property
    def target_temperature(self):
        for prop in self.data.get('properties'):
            if prop['id'] == 'SetpointTemperature':
                return float(prop['status'])

        return 0.0

    @property
    def minimum_temperature(self):
        for prop in self.data.get('properties'):
            if prop['id'] == 'SetpointTemperature':
                return float(prop['min'])

        return 0.0

    @property
    def maximum_temperature(self):
        for prop in self.data.get('properties'):
            if prop['id'] == 'SetpointTemperature':
                return float(prop['max'])

        return 0.0

    @property
    def temperature_steps(self):
        for prop in self.data.get('properties'):
            if prop['id'] == 'SetpointTemperature':
                return float(prop['step'])

        return 0.0

    def set_temperature(self, temperature):
        self.api.set_temperature(self.data, temperature)

    def set_operation_mode(self, operation):
        """ Set the operation mode. Either 'Heat' or 'Cool'"""
        self.api.set_operation_mode(self.data, operation)
