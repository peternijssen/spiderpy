from spiderpy.devices.base import SpiderDevice


class SpiderPowerPlug(SpiderDevice):
    @property
    def is_on(self) -> bool:
        return bool(self.data.get("isSwitchedOn"))

    @property
    def is_available(self) -> bool:
        return bool(self.data.get("isSwitchable"))

    @property
    def current_energy_consumption(self) -> float:
        current_usage = self.data.get("currentUsage")
        if current_usage is None:
            return 0.0

        return float(current_usage)

    @property
    def today_energy_consumption(self) -> float:
        today_usage = self.data.get("todayUsage")
        if today_usage is None:
            return 0.0

        return float(today_usage)

    def turn_on(self) -> bool:
        if self.is_online:
            self.data["isSwitchedOn"] = True
            return True
        return False

    def turn_off(self) -> bool:
        if self.is_online:
            self.data["isSwitchedOn"] = False
            return True
        return False

    def __str__(self) -> str:
        return f"{self.id} {self.name} {self.model} {self.manufacturer} {self.type} {self.is_online} {self.is_on} {self.is_available} {self.current_energy_consumption} {self.today_energy_consumption}"
