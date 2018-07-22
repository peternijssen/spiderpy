""" Python wrapper for the Spider API """

# TODO:
# - Rewrite access token handling
# - Catch API errors at all places
# - Redo retrieving todays energy usage from Power Plug
# - Power plug energy usage should set the timezone to UTC probably

import json
from datetime import datetime, timedelta
from urllib.parse import unquote

import requests

from spiderpy.devices.powerplug import SpiderPowerPlug
from spiderpy.devices.thermostat import SpiderThermostat

BASE_URL = 'https://mijn.ithodaalderop.nl'

AUTHENTICATE_URL = BASE_URL + '/api/tokens'
DEVICES_URL = BASE_URL + '/api/devices'
ENERGY_DEVICES_URL = BASE_URL + '/api/devices/energy/energyDevices'
POWER_PLUGS_URL = BASE_URL + '/api/devices/energy/smartPlugs'
ENERGY_MONITORING_URL = BASE_URL + '/api/monitoring/15/devices'


class SpiderApi(object):
    """ Interface class for the Spider API """

    def __init__(self, user, password):
        """ Constructor """

        self._user = user
        self._password = password
        self._thermostats = None
        self._power_plugs = None

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        payload = {
            'grant_type': 'password',
            'username': self._user,
            'password': self._password
        }

        try:
            response = requests.request(
                'POST', AUTHENTICATE_URL, data=payload, headers=headers)
            data = response.json()

        except Exception:
            raise (UnauthorizedException())

        if 'error' in data:
            raise UnauthorizedException(data['error'])

        self._access_token = data['access_token']
        self._refresh_token = unquote(data['refresh_token'])
        self._token_expires_in = data['expires_in']
        self._token_expires_at = datetime.now() + timedelta(0, data['expires_in'])

    def _is_token_expired(self):
        """ Check if access token is expired """
        if datetime.now() > self._token_expires_at:
            self._refresh_access_token()
            return True

        return False

    def _refresh_access_token(self):
        """ Refresh access_token """

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': self._refresh_token
        }

        response = requests.request(
            'POST', AUTHENTICATE_URL, data=payload, headers=headers)

        data = response.json()
        self._access_token = data['access_token']

    def get_thermostats(self, force_refresh=True):
        """ Retrieve thermostats """

        if self._thermostats is not None and force_refresh is False:
            return self._thermostats

        self._is_token_expired()
        self._thermostats = []

        headers = {
            'authorization': 'Bearer ' + self._access_token,
            'Content-Type': 'application/json'
        }

        response = requests.request(
            'GET', DEVICES_URL, headers=headers)

        if response.status_code == 401:
            self._refresh_access_token()
            thermostats = self.get_thermostats()
        else:
            thermostats = response.json()

        for thermostat in thermostats:
            if thermostat['type'] == 105:
                self._thermostats.append(SpiderThermostat(thermostat, self))

        return self._thermostats

    def set_temperature(self, thermostat, temperature):
        """ Set the temperature. Unfortunately, the API requires the complete object"""

        self._is_token_expired()

        for key, prop in enumerate(thermostat['properties']):
            # noinspection SpellCheckingInspection
            if prop['id'] == 'SetpointTemperature':
                thermostat['properties'][key]['status'] = temperature
                thermostat['properties'][key]['statusModified'] = True
                thermostat['properties'][key]['statusLastUpdated'] = str(datetime.now())

        headers = {
            'authorization': 'Bearer ' + self._access_token,
            'Content-Type': 'application/json'
        }

        response = requests.request(
            'PUT', DEVICES_URL + "/" + thermostat['id'], data=json.dumps(thermostat), headers=headers)

        if response.status_code == 401:
            self._refresh_access_token()
            self.set_temperature(thermostat, temperature)

        if response.status_code != 200:
            return False

        return True

    def set_operation_mode(self, thermostat, mode):
        """ Set the temperature. Unfortunately, the API requires the complete object"""

        self._is_token_expired()

        for key, prop in enumerate(thermostat['properties']):
            if prop['id'] == 'OperationMode':
                thermostat['properties'][key]['status'] = mode[0].upper() + mode[1:]
                thermostat['properties'][key]['statusModified'] = True
                thermostat['properties'][key]['statusLastUpdated'] = str(datetime.now())

        headers = {
            'authorization': 'Bearer ' + self._access_token,
            'Content-Type': 'application/json'
        }

        response = requests.request(
            'PUT', DEVICES_URL + "/" + thermostat['id'], data=json.dumps(thermostat), headers=headers)

        if response.status_code == 401:
            self._refresh_access_token()
            self.set_operation_mode(thermostat, mode)

        if response.status_code != 200:
            return False

        return True

    def get_power_plugs(self, force_refresh=False):
        """ Retrieve power plugs """

        if self._power_plugs is not None and force_refresh is False:
            return self._power_plugs

        self._is_token_expired()
        self._power_plugs = []

        headers = {
            'authorization': 'Bearer ' + self._access_token,
            'Content-Type': 'application/json'
        }

        response = requests.request(
            'GET', ENERGY_DEVICES_URL, headers=headers)

        if response.status_code == 401:
            self._refresh_access_token()
            power_plugs = self.get_power_plugs()
        else:
            power_plugs = response.json()

        for power_plug in power_plugs:
            if power_plug['isSwitch']:
                today = datetime.today().replace(hour=00, minute=00).strftime('%s')

                resp = requests.request(
                    'GET', ENERGY_MONITORING_URL + "/" + power_plug['id'] + "/?take=96&start=" + str(today) + "000", headers=headers)
                data = resp.json()

                power_plug['todayUsage'] = float(data[0]['totalEnergy']['normal']) + float(data[0]['totalEnergy']['low'])
                self._power_plugs.append(SpiderPowerPlug(power_plug, self))

        return self._power_plugs

    def turn_power_plug_on(self, power_plug_id):
        """ Turn the power_plug on"""

        self._is_token_expired()

        headers = {
            'authorization': 'Bearer ' + self._access_token,
            'Content-Type': 'application/json'
        }

        response = requests.request(
            'PUT', POWER_PLUGS_URL + power_plug_id + "/switch", data="true",
            headers=headers)

        if response.status_code == 401:
            self._refresh_access_token()
            self.turn_power_plug_on(power_plug_id)

        if response.status_code != 200:
            return False

        return True

    def turn_power_plug_off(self, power_plug_id):
        """ Turn the power plug off"""

        self._is_token_expired()

        headers = {
            'authorization': 'Bearer ' + self._access_token,
            'Content-Type': 'application/json'
        }

        response = requests.request(
            'PUT', POWER_PLUGS_URL + power_plug_id + "/switch", data="false",
            headers=headers)

        if response.status_code == 401:
            self._refresh_access_token()
            self.turn_power_plug_on(power_plug_id)

        if response.status_code != 200:
            return False

        return True


class UnauthorizedException(Exception):
    pass


class SpiderApiException(Exception):
    pass
