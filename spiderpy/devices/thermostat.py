from typing import Any, Dict, List

from spiderpy.devices.base import SpiderDevice


class SpiderThermostat(SpiderDevice):
    def __init__(self, data: Dict[Any, Any], api: Any) -> None:
        super().__init__(data, api)
        self.properties: List[Any] = []

        if self.data.get("properties") is not None:
            self.properties = self.data["properties"]

    @staticmethod
    def get_values(prop: Dict[Any, Any]) -> List[str]:
        values = []
        for choice in prop["scheduleChoices"]:
            if not choice["disabled"]:
                values.append(choice["value"])
        return values

    @property
    def operation_mode(self) -> str:
        for prop in self.properties:
            if prop["id"] == "OperationMode":
                return str(prop["status"])

        return "Idle"

    @property
    def operation_values(self) -> List[str]:
        values = []
        for prop in self.properties:
            if prop["id"] == "OperationMode":
                values = self.get_values(prop)
        return values

    @property
    def has_operation_mode(self) -> bool:
        for prop in self.properties:
            if prop["id"] == "OperationMode":
                return True

        return False

    @property
    def has_fan_mode(self) -> bool:
        for prop in self.properties:
            if prop["id"] == "FanSpeed":
                return True

        return False

    @property
    def fan_speed_values(self) -> List[str]:
        values = []
        for prop in self.properties:
            if prop["id"] == "FanSpeed":
                values = self.get_values(prop)
        return values

    @property
    def current_temperature(self) -> float:
        for prop in self.properties:
            if prop["id"] == "AmbientTemperature":
                return float(prop["status"])

        return 0.0

    @property
    def target_temperature(self) -> float:
        for prop in self.properties:
            if prop["id"] == "SetpointTemperature":
                return float(prop["status"])

        return 0.0

    @property
    def minimum_temperature(self) -> float:
        for prop in self.properties:
            if prop["id"] == "SetpointTemperature":
                return float(prop["min"])

        return 0.0

    @property
    def maximum_temperature(self) -> float:
        for prop in self.properties:
            if prop["id"] == "SetpointTemperature":
                return float(prop["max"])

        return 0.0

    @property
    def temperature_steps(self) -> float:
        for prop in self.properties:
            if prop["id"] == "SetpointTemperature":
                return float(prop["step"])

        return 0.0

    @property
    def current_fan_speed(self) -> str:
        for prop in self.properties:
            if prop["id"] == "FanSpeed":
                return str(prop["status"])

        return "Idle"

    def set_temperature(self, temperature: str) -> None:
        if self.is_online is True:
            self.api.set_temperature(self.data, temperature)

    def set_operation_mode(self, operation: str) -> None:
        """ Set the operation mode. Either 'Heat' or 'Cool'"""
        if self.is_online is True:
            self.api.set_operation_mode(self.data, operation)

    def set_fan_speed(self, fan_speed: str) -> bool:
        """ Set the fanspeed. Either 'Auto', 'Low', 'Medium', 'High', 'Boost 10', 'Boost 20', 'Boost 30'"""
        return self.is_online & self.api.set_fan_speed(self.data, fan_speed)

    def __str__(self) -> str:
        return f"{self.id} {self.name} {self.model} {self.manufacturer} {self.type} {self.is_online} {self.operation_mode} {self.operation_values} {self.has_operation_mode} {self.has_fan_mode} {self.fan_speed_values} {self.current_temperature} {self.target_temperature} {self.minimum_temperature} {self.maximum_temperature} {self.temperature_steps} {self.current_fan_speed}"
