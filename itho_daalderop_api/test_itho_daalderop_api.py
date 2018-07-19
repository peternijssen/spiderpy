import argparse
from itho_daalderop_api import IthoDaalderop_API


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Run the test for Itho Daalderop API")
    parser.add_argument(
        'username', type=str,
        help="Your email address")
    parser.add_argument(
        'password', type=str,
        help="Your password")
    args = parser.parse_args()
    username = args.username
    password = args.password
    ithodaalderop = IthoDaalderop_API(username, password)

    # Get thermostats
    print("Get thermostats")
    thermostats = ithodaalderop.get_thermostats()
    print("Number of thermostats: ", len(thermostats))
    print("Listing thermostats:")
    for thermostat in thermostats:
        print(thermostat['id'])
        print("Set temperature to 19 degrees")
        ithodaalderop.set_temperature(thermostat, 19)

    print("Retrieve from cache")
    thermostats = ithodaalderop.get_thermostats(False)
    for thermostat in thermostats:
        print(thermostat['id'])

    # Get powerplugs
    print("Get powerplugs")
    powerplugs = ithodaalderop.get_powerplugs()
    print("Number of powerplugs: ", len(powerplugs))
    print("Listing powerplugs:")
    for powerplug in powerplugs:
        print(powerplug['id'])

    print("Retrieve from cache")
    powerplugs = ithodaalderop.get_powerplugs(False)
    for powerplug in powerplugs:
        print(powerplug['id'])

if __name__ == '__main__':
    main()