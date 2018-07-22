import argparse

from spiderpy.spiderapi import SpiderApi


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
    api = SpiderApi(username, password)

    # Get thermostats
    # print("Get thermostats")
    thermostats = api.get_thermostats()
    print("Number of thermostats: ", len(thermostats))
    print("Listing thermostats:")
    for thermostat in thermostats:
        print(thermostat.id)
        print(thermostat.name)
        print(thermostat.current_temperature)
        print(thermostat.target_temperature)
        print(thermostat.minimum_temperature)
        print(thermostat.maximum_temperature)
        print("Set temperature to 19 degrees")
        thermostat.set_temperature(17)
        print("Set to cool")
        thermostat.set_operation_mode('Cool')

    print("Retrieve from cache")
    thermostats = api.get_thermostats(False)
    for thermostat in thermostats:
        print(thermostat.id)

    # Get power plugs
    print("Get power plugs")
    power_plugs = api.get_power_plugs()
    print("Number of power plugs: ", len(power_plugs))
    print("Listing power plugs:")
    for power_plug in power_plugs:
        print(power_plug.id)
        print(power_plug.name)
        print(power_plug.is_on)
        print(power_plug.current_energy_consumption)
        print("Turn on the power plug")
        power_plug.turn_on()

    print("Retrieve from cache")
    power_plugs = api.get_power_plugs(False)
    for power_plug in power_plugs:
        print(power_plug.id)


if __name__ == '__main__':
    main()
