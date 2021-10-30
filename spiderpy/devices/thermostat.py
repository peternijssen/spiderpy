from datetime import datetime
from typing import Any, Dict, List

from spiderpy.devices.base import SpiderDevice


class SpiderThermostat(SpiderDevice):
    @property
    def properties(self) -> List[Any]:
        if self.data.get("properties") is not None:
            return self.data["properties"]

        return []

    @property
    def current_operation_mode(self) -> str:
        for prop in self.properties:
            if prop["id"] == "OperationMode":
                return str(prop["status"])

        return "Idle"

    @property
    def has_operation_mode(self) -> bool:
        for prop in self.properties:
            if prop["id"] == "OperationMode":
                return True

        return False

    @property
    def available_operation_modes(self) -> List[str]:
        operation_modes = []
        for prop in self.properties:
            if prop["id"] == "OperationMode":
                operation_modes = self.get_values(prop)

        return operation_modes

    @property
    def current_fan_speed_mode(self) -> str:
        for prop in self.properties:
            if prop["id"] == "FanSpeed":
                return str(prop["status"])

        return "Idle"

    @property
    def has_fan_speed_mode(self) -> bool:
        for prop in self.properties:
            if prop["id"] == "FanSpeed":
                return True

        return False

    @property
    def available_fan_speed_modes(self) -> List[str]:
        fan_speeds = []
        for prop in self.properties:
            if prop["id"] == "FanSpeed":
                fan_speeds = self.get_values(prop)

        return fan_speeds

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

    def set_operation_mode(self, operation_mode: str) -> bool:
        """ Set the operation mode. Either 'Heat' or 'Cool'"""
        if self.is_online:
            self.reset_last_modified()

            for prop in self.properties:
                if prop["id"] == "OperationMode":
                    prop["status"] = operation_mode[0].upper() + operation_mode[1:]
                    prop["statusModified"] = True
                    prop["statusLastUpdated"] = str(datetime.now())
                    return True

        return False

    def set_fan_speed(self, fan_speed: str) -> bool:
        """ Set the fan speed. Either 'Auto', 'Low', 'Medium', 'High', 'Boost 10', 'Boost 20', 'Boost 30'"""
        if self.is_online:
            self.reset_last_modified()

            for prop in self.properties:
                if prop["id"] == "FanSpeed":
                    prop["status"] = fan_speed[0].upper() + fan_speed[1:]
                    prop["statusModified"] = True
                    prop["statusLastUpdated"] = str(datetime.now())
                    return True

        return False

    def set_temperature(self, temperature: float) -> bool:
        if self.is_online:
            self.reset_last_modified()

            for prop in self.properties:
                if prop["id"] == "SetpointTemperature":
                    prop["status"] = str(temperature)
                    prop["statusModified"] = True
                    prop["statusLastUpdated"] = str(datetime.now())
                    return True

        return False

    @staticmethod
    def get_values(prop: Dict[Any, Any]) -> List[str]:
        values = []
        for choice in prop["scheduleChoices"]:
            if not choice["disabled"]:
                values.append(choice["value"])
        return values

    def reset_last_modified(self) -> None:
        for prop in self.properties:
            if prop.get("statusModified", False):
                prop["statusModified"] = False

    def __str__(self) -> str:
        return f"{self.id} {self.name} {self.model} {self.manufacturer} {self.type} {self.is_online} {self.current_operation_mode} {self.has_operation_mode} {self.available_operation_modes} {self.current_fan_speed_mode} {self.has_fan_speed_mode} {self.available_fan_speed_modes} {self.current_temperature} {self.target_temperature} {self.minimum_temperature} {self.maximum_temperature} {self.temperature_steps}"
