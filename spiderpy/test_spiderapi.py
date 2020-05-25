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
        print(thermostat)
        print("Set temperature to 19 degrees")
        thermostat.set_temperature(19)

        if thermostat.has_operation_mode:
            print("Set to cool")
            thermostat.set_operation_mode('Cool')
            print("Set to heat")
            thermostat.set_operation_mode('Heat')
        if thermostat.has_fan_mode:
            print("Set fan speed to auto")
            thermostat.set_fan_speed('Auto')

    if unique_id is not None:
        print("Retrieve by id")
        thermostat = api.get_thermostat(unique_id)
        print(thermostat)

    time.sleep(10)

    # Get power plugs
    unique_id = None
    print("Get power plugs")
    power_plugs = api.get_power_plugs()
    print("Number of power plugs: ", len(power_plugs))
    print("Listing power plugs:")
    for power_plug in power_plugs:
        print(power_plug)
        print("Turn on the power plug")
        power_plug.turn_on()

    if unique_id is not None:
        print("Retrieve by id")
        power_plug = api.get_power_plug(unique_id)
        print(power_plug)


if __name__ == '__main__':
    main()
