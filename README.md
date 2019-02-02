# SpiderPy
Unofficial Python wrapper for the Spider API, to control your Spider installation.
Use the same credentials as the ones you use at [https://mijn.ithodaalderop.nl ](https://mijn.ithodaalderop.nl )

This library is not affiliated with Itho Daalderop or Spider and retrieves date from the endpoints of the mobile application. Use at your own risk.

## Currently supports

**Thermostat**
- Viewing the current and target temperature
- Changing operation mode to Heat or Cool
- Changing the fan speed

**Power Plugs**
- Viewing the energy usage and the state of power plugs
- Enabling or disabling power plug

All other elements like ventilation are not supported purely because my home does not support this. So I am missing a valid test case.
Same goes for all the upcoming Spider expansions.

## Home Assistant
This library is being used in [Home Assistant](https://www.home-assistant.io/components/spider/) as a component.

## More information about Spider (Dutch)
[http://www.ithodaalderop.nl/spider-thermostaat/wat-is-spider](http://www.ithodaalderop.nl/spider-thermostaat/wat-is-spider)

## Contributors
* [Peter Nijssen](https://github.com/peternijssen)
* [Stefan Oude Vrielink](https://github.com/soudevrielink)
