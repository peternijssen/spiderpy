import argparse
import time

from spiderpy import SpiderApi


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Run some live tests against the API")
    parser.add_argument(
        'username', type=str,
        help="Your email address")
    parser.add_argument(
        'password', type=str,
        help="Your password")
    args = parser.parse_args()
    username = args.username
    password = args.password
    api = SpiderApi(username, password, 5)
    unique_id = None

    # Get thermostats
    print("Get thermostats")
    thermostats = api.get_thermostats()
    print("Number of thermostats: ", len(thermostats))
    print("Listing thermostats:")
    for thermostat in thermostats:
        print("ID: " + thermostat.id)
        print("Name: " + thermostat.name)
        print("Operation mode: " + thermostat.operation_mode)
        print("Current Temperature: " + str(thermostat.current_temperature))
        print("Target Temperature: " + str(thermostat.target_temperature))
        print("Minimum Temperature: " + str(thermostat.minimum_temperature))
        print("Maximum Temperature: " + str(thermostat.maximum_temperature))
        print("Set temperature to 19 degrees")
        thermostat.set_temperature(19)
        print("Set to cool")
        thermostat.set_operation_mode('Cool')

    print("Retrieve from cache")
    thermostats = api.get_thermostats()
    for thermostat in thermostats:
        print("ID: " + thermostat.id)
        unique_id = thermostat.id

    print("Retrieve by id")
    thermostat = api.get_thermostat(unique_id)
    print("ID: " + thermostat.id)

    time.sleep(10)

    # Get power plugs
    print("Get power plugs")
    power_plugs = api.get_power_plugs()
    print("Number of power plugs: ", len(power_plugs))
    print("Listing power plugs:")
    for power_plug in power_plugs:
        print("ID: " + power_plug.id)
        print("Name: " + power_plug.name)
        print("Enabled: " + str(power_plug.is_on))
        print("Available: " + str(power_plug.is_available))
        print("Current Energy Consumption: " + str(power_plug.current_energy_consumption))
        print("Today Energy Consumption: " + str(power_plug.today_energy_consumption))
        print("Turn on the power plug")
        power_plug.turn_on()

    print("Retrieve from cache")
    power_plugs = api.get_power_plugs()
    for power_plug in power_plugs:
        print("ID: " + power_plug.id)
        unique_id = power_plug.id

    print("Retrieve by id")
    power_plug = api.get_power_plug(unique_id)
    print("ID: " + power_plug.id)


if __name__ == '__main__':
    main()
