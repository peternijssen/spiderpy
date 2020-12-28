from spiderpy.devices.base import SpiderDevice


# noinspection SpellCheckingInspection
class SpiderThermostat(SpiderDevice):
    def get_values(self, property):
        values = []
        for choice in property['scheduleChoices']:
            if not choice['disabled']:
                values.append(choice['value'])
        return values

    @property
    def operation_mode(self):
        for prop in self.data.get('properties'):
            if prop['id'] == 'OperationMode':
                return prop['status']

        return "Idle"

    @property
    def operation_values(self):
        values = []
        for prop in self.data.get('properties'):
            if prop['id'] == 'OperationMode':
                values = self.get_values(prop)
        return values

    @property
    def has_operation_mode(self):
        for prop in self.data.get('properties'):
            if prop['id'] == 'OperationMode':
                return True

        return False

    @property
    def has_fan_mode(self):
        for prop in self.data.get('properties'):
            if prop['id'] == 'FanSpeed':
                return True

        return False

    @property
    def fan_speed_values(self):
        values = []
        for prop in self.data.get('properties'):
            if prop['id'] == 'FanSpeed':
                values = self.get_values(prop)
        return values

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

    @property
    def current_fan_speed(self):
        for prop in self.data.get('properties'):
            if prop['id'] == 'FanSpeed':
                return prop['status']

        return "Idle"

    def set_temperature(self, temperature):
        if self.is_online is True:
            self.api.set_temperature(self.data, temperature)

    def set_operation_mode(self, operation):
        """ Set the operation mode. Either 'Heat' or 'Cool'"""
        if self.is_online is True:
            self.api.set_operation_mode(self.data, operation)

    def set_fan_speed(self, fanspeed):
        """ Set the fanspeed. Either 'Auto', 'Low', 'Medium', 'High', 'Boost 10', 'Boost 20', 'Boost 30'"""
        return self.is_online & self.api.set_fan_speed(self.data, fanspeed)

    def __str__(self):
        return f"{self.id} {self.name} {self.model} {self.manufacturer} {self.type} {self.is_online} {self.operation_mode} {self.has_operation_mode} {self.has_fan_mode} {self.current_temperature} {self.target_temperature} {self.minimum_temperature} {self.maximum_temperature} {self.temperature_steps} {self.current_fan_speed}"