import argparse

from spiderpy.spiderapi import SpiderApi


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Run some live tests against the API")
    parser.add_argument("username", type=str, help="Your email address")
    parser.add_argument("password", type=str, help="Your password")
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
        temp_target_curr = thermostat.target_temperature
        temp_list = [(temp_target_curr - 1), temp_target_curr]
        for temp in temp_list:
            print("Set temperature to " + str(temp) + " degrees")
            # thermostat.set_temperature(temp)
            # assert (temp == thermostat.target_temperature), "Failed to set target temperature"

        if thermostat.has_operation_mode:
            operation_mode_list = thermostat.operation_values
            if operation_mode_list[-1] != thermostat.operation_mode:
                operation_mode_list.reverse()
            for operation_mode in operation_mode_list:
                print("Set to " + operation_mode)
                # thermostat.set_operation_mode(operation_mode)
                # assert (thermostat.operation_mode == operation_mode), "Failed to set operation mode"

        if thermostat.has_fan_mode:
            fan_speed_curr = thermostat.current_fan_speed
            print("Current fan speed: " + str(fan_speed_curr))
            speed_list = thermostat.fan_speed_values
            speed_list.reverse()
            for speed in speed_list:
                print("Set fan speed to " + speed)
                speed_set = thermostat.set_fan_speed(speed)
                assert speed_set & (thermostat.current_fan_speed == speed), "Failed to set fan speed"

            if fan_speed_curr is not None:
                print("Set fan speed back to " + str(fan_speed_curr))
                thermostat.set_fan_speed(fan_speed_curr)

    if unique_id is not None:
        print("Retrieve by id")
        thermostat = api.get_thermostat(unique_id)
        print(thermostat)

    # Get power plugs
    unique_id = None
    print("Get power plugs")
    power_plugs = api.get_power_plugs()
    print("Number of power plugs: ", len(power_plugs))
    print("Listing power plugs:")
    for power_plug in power_plugs:
        print(power_plug)
        print("Turn on the power plug")
        # power_plug.turn_on()

    if unique_id is not None:
        print("Retrieve by id")
        power_plug = api.get_power_plug(unique_id)
        print(power_plug)


if __name__ == "__main__":
    main()
