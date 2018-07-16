""" Python wrapper for the IthoDaalderop API """

from datetime import datetime, timedelta
from random import randint

import json
import requests

BASE_URL = 'https://mijn.ithodaalderop.nl'

AUTHENTICATE_URL = BASE_URL + '/api/tokens'
DEVICES_URL = BASE_URL + '/api/devices'


class UnauthorizedException(Exception):
    pass


class IthoDaalderop_API(object):
    """ Interface class for the IthoDaalderop API """

    def __init__(self, user, password):
        """ Constructor """

        self._user = user
        self._password = password

        payload = {
            'grant_type': 'password',
            'username': self._user,
            'password': self._password
        }

        try:
            response = requests.request(
                'POST', AUTHENTICATE_URL, data=payload)
            data = response.json()

        except Exception:
            raise(UnauthorizedException())

        if 'error' in data:
            raise UnauthorizedException(data['error'])

        self._access_token = data['access_token']
        self._refresh_token = data['refresh_token']
        self._token_expires_in = data['expires_in']
        self._token_expires_at = datetime.now(
        ) + timedelta(0, data['expires_in'])

    def _is_token_expired(self):
        """ Check if access token is expired """
        if (datetime.now() > self._token_expires_at):
            self._refresh_access_token()
            return True

        return False

    def _refresh_access_token(self):
        """ Refresh access_token """

        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': self._refresh_token
        }

        response = requests.request(
            'POST', AUTHENTICATE_URL, data=payload)

        data = response.json()

        self._access_token = data['access_token']

    def get_thermostats(self):
        """ Retrieve thermostats """

        self._is_token_expired()

        headers = {
            'authorization': 'Bearer ' + self._access_token
        }

        response = requests.request(
            'GET', DEVICES_URL, headers=headers)

        if response.status_code == 401:
            self._refresh_access_token()
            thermostats = self.get_thermostats()
        else:
            thermostats = response.json()

        # 105 == Spider thermostat
        thermostats = [x for x in thermostats if x['type'] == 105]

        return thermostats

    def set_temperature(self, thermostat, temperature):
        """ Set the temperature. Unfortunately, the API requires the complete object"""

        self._is_token_expired()

        for key, prop in enumerate(thermostat['properties']):
            if prop['id'] == 'SetpointTemperature':
                thermostat['properties'][key]['status'] = temperature
                thermostat['properties'][key]['statusModified'] = True
                thermostat['properties'][key]['statusLastUpdated'] = str(datetime.now())

        thermostat['_etag'] = randint(10000000, 99999999)
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

    def get_powerplugs(self):
        """ Retrieve powerplugs """

        self._is_token_expired()

        headers = {
            'authorization': 'Bearer ' + self._access_token
        }

        response = requests.request(
            'GET', DEVICES_URL, headers=headers)

        if response.status_code == 401:
            self._refresh_access_token()
            powerplugs = self.get_powerplugs()
        else:
            powerplugs = response.json()

        # 105 == Spider powerplug
        powerplugs = [x for x in powerplugs if x['type'] == 103]

        return powerplugs