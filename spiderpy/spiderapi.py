""" Python wrapper for the Spider API """
from __future__ import annotations

import json
import logging
import time
from datetime import datetime, timedelta
from typing import Any, Dict, ValuesView
from urllib.parse import unquote

import requests

from spiderpy.devices.powerplug import SpiderPowerPlug
from spiderpy.devices.thermostat import SpiderThermostat

BASE_URL = "https://spider-api.ithodaalderop.nl"

AUTHENTICATE_URL = BASE_URL + "/api/tokens"
DEVICES_URL = BASE_URL + "/api/devices"
ENERGY_DEVICES_URL = BASE_URL + "/api/devices/energy/energyDevices"
POWER_PLUGS_URL = BASE_URL + "/api/devices/energy/smartPlugs"
ENERGY_MONITORING_URL = BASE_URL + "/api/monitoring/15/devices"

REFRESH_RATE = 120

_LOGGER = logging.getLogger(__name__)


class SpiderApi:
    """ Interface class for the Spider API """

    def __init__(
        self, username: str, password: str, refresh_rate: int = REFRESH_RATE
    ) -> None:
        """ Constructor """
        self._username = ""
        for char in username:
            self._username += hex(ord(char)).lstrip("0x")
        self._password = password
        self._thermostats: Dict[Any, Any] = {}
        self._power_plugs: Dict[Any, Any] = {}
        self._last_refresh = 0
        self._access_token = ""
        self._refresh_token = ""
        self._token_expires_at = datetime.now() - timedelta(days=1)
        self._token_expires_in = None
        self._refresh_rate = refresh_rate

    def _reset_status_modified(self, thermostat: Dict[str, Any]) -> None:
        """ Reset all statusModified to false """
        for key in enumerate(thermostat["properties"]):
            # noinspection SpellCheckingInspection
            if thermostat["properties"][key].get("statusModified", False):
                thermostat["properties"][key]["statusModified"] = False

    def update(self) -> None:
        """ Update the cache """
        current_time = int(time.time())
        last_refresh = 0 if self._last_refresh is None else self._last_refresh

        if current_time >= (last_refresh + self._refresh_rate):
            self.update_thermostats()
            self.update_power_plugs()

            self._last_refresh = int(time.time())

    def update_thermostats(self) -> None:
        """ Retrieve thermostats """
        results = self._request_update(DEVICES_URL)

        if results is False:
            return

        for thermostat in results:
            if thermostat["type"] == 105:
                self._thermostats[thermostat["id"]] = SpiderThermostat(thermostat, self)

    def get_thermostats(self) -> ValuesView[SpiderThermostat]:
        """ Get all thermostats """
        self.update()

        return self._thermostats.values()

    def get_thermostat(self, unique_id: str) -> SpiderThermostat | None:
        """ Get a thermostat by id """
        self.update()

        if unique_id in self._thermostats:
            return self._thermostats[unique_id]

        return None

    def set_temperature(self, thermostat: Dict[Any, Any], temperature: float) -> bool:
        """ Set the temperature. Unfortunately, the API requires the complete object"""
        self._reset_status_modified(
            thermostat
        )  # Make sure only temperature will be modified
        for key, prop in enumerate(thermostat["properties"]):
            # noinspection SpellCheckingInspection
            if prop["id"] == "SetpointTemperature":
                thermostat["properties"][key]["status"] = temperature
                thermostat["properties"][key]["statusModified"] = True
                thermostat["properties"][key]["statusLastUpdated"] = str(datetime.now())

        url = DEVICES_URL + "/" + thermostat["id"]
        try:
            return self._request_action(url, json.dumps(thermostat))
        except SpiderApiException:
            _LOGGER.error(f"Unable to set temperature to {temperature}.")
        return False

    def set_operation_mode(self, thermostat: Dict[Any, Any], mode: str) -> bool:
        """ Set the operation mode. Unfortunately, the API requires the complete object"""
        self._reset_status_modified(
            thermostat
        )  # Make sure only operation mode will be modified
        for key, prop in enumerate(thermostat["properties"]):
            if prop["id"] == "OperationMode":
                thermostat["properties"][key]["status"] = mode[0].upper() + mode[1:]
                thermostat["properties"][key]["statusModified"] = True
                thermostat["properties"][key]["statusLastUpdated"] = str(datetime.now())

        url = DEVICES_URL + "/" + thermostat["id"]
        try:
            return self._request_action(url, json.dumps(thermostat))
        except SpiderApiException:
            _LOGGER.error(
                f"Unable to set operation mode to {mode}. Is this operation mode supported?"
            )
        return False

    def set_fan_speed(self, thermostat: Dict[Any, Any], fan_speed: str) -> bool:
        """ Set the fan speed. Unfortunately, the API requires the complete object"""
        self._reset_status_modified(
            thermostat
        )  # Make sure only fan speed will be modified
        for key, prop in enumerate(thermostat["properties"]):
            # noinspection SpellCheckingInspection
            if prop["id"] == "FanSpeed":
                thermostat["properties"][key]["status"] = (
                    fan_speed[0].upper() + fan_speed[1:]
                )
                thermostat["properties"][key]["statusModified"] = True
                thermostat["properties"][key]["statusLastUpdated"] = str(datetime.now())

        url = DEVICES_URL + "/" + thermostat["id"]
        try:
            return self._request_action(url, json.dumps(thermostat))
        except SpiderApiException:
            _LOGGER.error(
                f"Unable to set fan speed to {fan_speed}. Is this fan speed supported?"
            )
        return False

    def update_power_plugs(self) -> None:
        """ Retrieve power plugs """
        results = self._request_update(ENERGY_DEVICES_URL)

        if results is False:
            return

        for power_plug in results:
            if power_plug["isSwitch"]:
                today = (
                    datetime.today()
                    .replace(hour=00, minute=00, second=00)
                    .strftime("%s")
                )

                energy_url = (
                    ENERGY_MONITORING_URL
                    + "/"
                    + power_plug["energyDeviceId"]
                    + "/?take=96&start="
                    + str(today)
                    + "000"
                )
                energy_results = self._request_update(energy_url)

                if energy_results is False:
                    continue

                try:
                    power_plug["todayUsage"] = float(
                        energy_results[0]["totalEnergy"]["normal"]
                    ) + float(energy_results[0]["totalEnergy"]["low"])
                except IndexError:
                    _LOGGER.error("Unable to get today energy usage for power plug")

                self._power_plugs[power_plug["id"]] = SpiderPowerPlug(power_plug, self)

    def get_power_plugs(self) -> ValuesView[SpiderPowerPlug]:
        """ Get all power plugs """
        self.update()

        return self._power_plugs.values()

    def get_power_plug(self, unique_id: str) -> SpiderPowerPlug | None:
        """ Get a power plug by id """
        self.update()

        if unique_id in self._power_plugs:
            return self._power_plugs[unique_id]

        return None

    def turn_power_plug_on(self, power_plug_id: str) -> bool:
        """ Turn the power_plug on"""
        url = POWER_PLUGS_URL + "/" + power_plug_id + "/switch"
        try:
            return self._request_action(url, "true")
        except SpiderApiException:
            _LOGGER.error("Unable to turn power plug on.")
        return False

    def turn_power_plug_off(self, power_plug_id: str) -> bool:
        """ Turn the power plug off"""
        url = POWER_PLUGS_URL + "/" + power_plug_id + "/switch"
        try:
            return self._request_action(url, "false")
        except SpiderApiException:
            _LOGGER.error("Unable to turn power plug off.")
        return False

    def _is_authenticated(self) -> bool:
        """ Check if access token is expired """
        if self._refresh_token == "":
            self._request_login()

        if datetime.now() > self._token_expires_at:
            self._refresh_access_token()
            return True

        return False

    def _request_action(self, url: str, data: str) -> bool:
        """ Perform a request to execute an action """
        self._is_authenticated()

        headers = {
            "authorization": "Bearer " + self._access_token,
            "Content-Type": "application/json",
            "X-Client-Platform": "android-phone",
            "X-Client-Version": "1.5.9 (3611)",
            "X-Client-Library": "SpiderPy",
        }

        try:
            response = requests.request("PUT", url, data=data, headers=headers)
        except Exception as exception:
            raise SpiderApiException(exception) from exception

        if response.status_code == 401:
            raise SpiderApiException("Access denied. Failed to refresh?")

        if response.status_code != 200:
            raise SpiderApiException(
                f"Unable to perform action. Status code: {response.status_code}. Data: {data}"
            )

        return True

    def _request_update(self, url: str) -> Dict[Any, Any]:
        """ Perform a request to update information """
        self._is_authenticated()

        headers = {
            "authorization": "Bearer " + self._access_token,
            "Content-Type": "application/json",
            "X-Client-Platform": "android-phone",
            "X-Client-Version": "1.5.9 (3611)",
            "X-Client-Library": "SpiderPy",
        }

        try:
            response = requests.request("GET", url, headers=headers)
        except Exception as exception:
            raise SpiderApiException(exception) from exception

        if response.status_code == 401:
            raise SpiderApiException("Access denied. Failed to refresh?")

        if response.status_code != 200:
            raise SpiderApiException(
                f"Unable to request update. Status code: {response.status_code}"
            )

        return response.json()

    def _request_login(self) -> None:
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Client-Platform": "android-phone",
            "X-Client-Version": "1.5.9 (3611)",
            "X-Client-Library": "SpiderPy",
        }

        payload = {
            "grant_type": "password",
            "username": self._username,
            "password": self._password,
        }

        try:
            response = requests.request(
                "POST", AUTHENTICATE_URL, data=payload, headers=headers
            )
        except Exception as exception:
            raise UnauthorizedException(exception) from exception

        if response.status_code != 200:
            raise SpiderApiException(
                f"Unable to request login. Status code: {response.status_code}"
            )

        data = response.json()
        self._access_token = data["access_token"]
        self._refresh_token = unquote(data["refresh_token"])
        self._token_expires_in = data["expires_in"]
        self._token_expires_at = datetime.now() + timedelta(
            0, (int(data["expires_in"]) - 20)
        )

    def _refresh_access_token(self) -> None:
        """ Refresh access_token """

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Client-Platform": "android-phone",
            "X-Client-Version": "1.5.9 (3611)",
            "X-Client-Library": "SpiderPy",
        }

        payload = {"grant_type": "refresh_token", "refresh_token": self._refresh_token}

        response = requests.request(
            "POST", AUTHENTICATE_URL, data=payload, headers=headers
        )

        data = response.json()

        if response.status_code != 200:
            raise SpiderApiException(
                f"Unable to refresh access token. Status code: {response.status_code}"
            )

        self._access_token = data["access_token"]
        self._refresh_token = unquote(data["refresh_token"])
        self._token_expires_in = data["expires_in"]
        self._token_expires_at = datetime.now() + timedelta(
            0, (int(data["expires_in"]) - 20)
        )


class UnauthorizedException(Exception):
    pass


class SpiderApiException(Exception):
    pass
