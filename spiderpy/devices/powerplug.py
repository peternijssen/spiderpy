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
        self.api.turn_power_plug_on(self.id)

    def turn_off(self):
        self.api.turn_power_plug_off(self.id)
