""" Python wrapper for the Spider API """

import json
import time
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

REFRESH_RATE = 120


class SpiderApi(object):
    """ Interface class for the Spider API """

    def __init__(self, user, password, refresh_rate=REFRESH_RATE):
        """ Constructor """

        self._user = user
        self._password = password
        self._thermostats = {}
        self._power_plugs = {}
        self._last_refresh = None
        self._refresh_rate = refresh_rate
        self._login()

    def _login(self):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Client-Platform': 'android-phone',
            'X-Client-Version': '1.5.3 (3561)',
            'X-Client-Library': 'SpiderPy'
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
        self._token_expires_at = datetime.now() + timedelta(0, (int(data['expires_in']) - 20))

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
            'X-Client-Platform': 'android-phone',
            'X-Client-Version': '1.5.3 (3561)',
            'X-Client-Library': 'SpiderPy'
        }

        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': self._refresh_token
        }

        response = requests.request(
            'POST', AUTHENTICATE_URL, data=payload, headers=headers)

        data = response.json()

        if response.status_code != 200:
            self._login()
        else:
            self._access_token = data['access_token']
            self._refresh_token = unquote(data['refresh_token'])
            self._token_expires_in = data['expires_in']
            self._token_expires_at = datetime.now() + timedelta(0, (int(data['expires_in']) - 20))

    def update(self):
        """ Update the cache """
        self._is_token_expired()

        current_time = int(time.time())
        last_refresh = 0 if self._last_refresh is None else self._last_refresh

        if current_time >= (last_refresh + self._refresh_rate):
            self.update_thermostats()
            self.update_power_plugs()

            self._last_refresh = int(time.time())

    def update_thermostats(self):
        """ Retrieve thermostats """
        headers = {
            'authorization': 'Bearer ' + self._access_token,
            'Content-Type': 'application/json',
            'X-Client-Platform': 'android-phone',
            'X-Client-Version': '1.5.3 (3561)',
            'X-Client-Library': 'SpiderPy'
        }

        response = requests.request(
            'GET', DEVICES_URL, headers=headers)

        if response.status_code == 401:
            self._refresh_access_token()
            self.update_thermostats()
        else:
            results = response.json()

            for thermostat in results:
                if thermostat['type'] == 105:
                    self._thermostats[thermostat['id']] = SpiderThermostat(thermostat, self)

    def get_thermostats(self):
        """ Get all thermostats """
        self.update()

        return self._thermostats.values()

    def get_thermostat(self, id):
        """ Get a thermostat by id """
        self.update()

        if id in self._thermostats:
            return self._thermostats[id]

        return None

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
            'Content-Type': 'application/json',
            'X-Client-Platform': 'android-phone',
            'X-Client-Version': '1.5.3 (3561)',
            'X-Client-Library': 'SpiderPy'
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
            'Content-Type': 'application/json',
            'X-Client-Platform': 'android-phone',
            'X-Client-Version': '1.5.3 (3561)',
            'X-Client-Library': 'SpiderPy'
        }

        response = requests.request(
            'PUT', DEVICES_URL + "/" + thermostat['id'], data=json.dumps(thermostat), headers=headers)

        if response.status_code == 401:
            self._refresh_access_token()
            self.set_operation_mode(thermostat, mode)

        if response.status_code != 200:
            return False

        return True

    def update_power_plugs(self):
        """ Retrieve power plugs """
        headers = {
            'authorization': 'Bearer ' + self._access_token,
            'Content-Type': 'application/json',
            'X-Client-Platform': 'android-phone',
            'X-Client-Version': '1.5.3 (3561)',
            'X-Client-Library': 'SpiderPy'
        }

        response = requests.request(
            'GET', ENERGY_DEVICES_URL, headers=headers)

        if response.status_code == 401:
            self._refresh_access_token()
            self.update_power_plugs()
        else:
            results = response.json()

            for power_plug in results:
                if power_plug['isSwitch']:
                    today = datetime.today().replace(hour=00, minute=00).strftime('%s')

                    resp = requests.request(
                        'GET', ENERGY_MONITORING_URL + "/" + power_plug['id'] + "/?take=96&start=" + str(today) + "000",
                        headers=headers)
                    data = resp.json()

                    power_plug['todayUsage'] = float(data[0]['totalEnergy']['normal']) + float(
                        data[0]['totalEnergy']['low'])
                    self._power_plugs[power_plug['id']] = (SpiderPowerPlug(power_plug, self))

    def get_power_plugs(self):
        """ Get all power plugs """
        self.update()

        return self._power_plugs.values()

    def get_power_plug(self, id):
        """ Get a power plug by id """
        self.update()

        if id in self._power_plugs:
            return self._power_plugs[id]

        return None

    def turn_power_plug_on(self, power_plug_id):
        """ Turn the power_plug on"""

        self._is_token_expired()

        headers = {
            'authorization': 'Bearer ' + self._access_token,
            'Content-Type': 'application/json',
            'X-Client-Platform': 'android-phone',
            'X-Client-Version': '1.5.3 (3561)',
            'X-Client-Library': 'SpiderPy'
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
            'Content-Type': 'application/json',
            'X-Client-Platform': 'android-phone',
            'X-Client-Version': '1.5.3 (3561)',
            'X-Client-Library': 'SpiderPy'
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
