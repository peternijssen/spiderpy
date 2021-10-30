from typing import Any, Dict


class SpiderDevice:
    def __init__(self, data: Dict[Any, Any]) -> None:
        self.data = data

    @property
    def id(self) -> str:
        return str(self.data.get("id"))

    @property
    def name(self) -> str:
        return str(self.data.get("name"))

    @property
    def model(self) -> str:
        return str(self.data.get("model"))

    @property
    def manufacturer(self) -> str:
        return str(self.data.get("manufacturer"))

    @property
    def type(self) -> int:
        # 105 == Thermostat
        # 103 == PowerPlug
        # 200 == Energy Devices (Also contains PowerPlug)
        device_type = self.data.get("type")
        if device_type is None:
            return 0
        return int(device_type)

    @property
    def is_online(self) -> bool:
        return bool(self.data.get("isOnline"))
