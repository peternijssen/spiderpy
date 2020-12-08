from spiderpy.devices.base import SpiderDevice


class SpiderPowerPlug(SpiderDevice):

    @property
    def is_on(self):
        return self.data.get('isSwitchedOn')

    @property
    def is_available(self):
        return self.data.get('isSwitchable')

    @property
    def current_energy_consumption(self):
        return self.data.get('currentUsage')

    @property
    def today_energy_consumption(self):
        return self.data.get('todayUsage')

    def turn_on(self):
        if self.is_online is True:
            self.data['isSwitchedOn'] = True
            self.api.turn_power_plug_on(self.id)

    def turn_off(self):
        if self.is_online is True:
            self.data['isSwitchedOn'] = False
            self.api.turn_power_plug_off(self.id)

    def __str__(self):
        return f"{self.id} {self.name} {self.model} {self.manufacturer} {self.type} {self.is_online} {self.is_on} {self.is_available} {self.current_energy_consumption} {self.today_energy_consumption}"