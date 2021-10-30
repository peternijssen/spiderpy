import argparse

from spiderpy.spiderapi import SpiderApi


def main() -> None:
    """Main function."""
    parser = argparse.ArgumentParser(description="Run some live tests against the API")
    parser.add_argument("username", type=str, help="Your email address")
    parser.add_argument("password", type=str, help="Your password")
    args = parser.parse_args()
    username = args.username
    password = args.password
    api = SpiderApi(username, password, 5)

    # Get thermostats
    print("Get thermostats")
    thermostats = api.get_thermostats()
    print("Number of thermostats: ", len(thermostats))
    print("Listing thermostats:")
    for thermostat in thermostats:
        print(thermostat)
        temp_target_curr = thermostat.target_temperature
        temp_list = [(temp_target_curr - 1), temp_target_curr]
        for temp in temp_list:
            print("Set temperature to " + str(temp) + " degrees")
            api.set_temperature(thermostat, temp)
            assert (
                temp == thermostat.target_temperature
            ), "Failed to set target temperature"

        if thermostat.has_operation_mode:
            operation_mode_list = thermostat.available_operation_modes
            if operation_mode_list[-1] != thermostat.current_operation_mode:
                operation_mode_list.reverse()
            for operation_mode in operation_mode_list:
                print("Set to " + operation_mode)
                # api.set_operation_mode(thermostat, operation_mode)
                # assert (thermostat.operation_mode == operation_mode), "Failed to set operation mode"

        if thermostat.has_fan_speed_mode:
            fan_speed_curr = thermostat.current_fan_speed_mode
            print("Current fan speed: " + str(fan_speed_curr))
            speed_list = thermostat.available_fan_speed_modes
            speed_list.reverse()
            for speed in speed_list:
                print("Set fan speed to " + speed)
                speed_set = api.set_fan_speed(thermostat, speed)
                assert speed_set & (
                    thermostat.current_fan_speed_mode == speed
                ), "Failed to set fan speed"

            if fan_speed_curr is not None:
                print("Set fan speed back to " + str(fan_speed_curr))
                thermostat.set_fan_speed(fan_speed_curr)
        print("Retrieve by id")
        print(api.get_thermostat(thermostat.id))
        print("")

    # Get power plugs
    print("Get power plugs")
    power_plugs = api.get_power_plugs()
    print("Number of power plugs: ", len(power_plugs))
    print("Listing power plugs:")
    for power_plug in power_plugs:
        print(power_plug)
        print("Turn on the power plug")
        # api.turn_power_plug_on(power_plug)
        print("Retrieve by id")
        print(api.get_power_plug(power_plug.id))
        print("")


if __name__ == "__main__":
    main()
