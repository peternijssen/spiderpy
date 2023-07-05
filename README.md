# ARCHIVED  
The spider application is no longer available as of September 1st, 2023. Therefor it has no use anymore to maintain this library.
See https://github.com/peternijssen/spiderpy/issues/120

# SpiderPy
Unofficial Python wrapper for the Spider API, to control your Spider installation.
Use the same credentials as the ones you use at [https://mijn.ithodaalderop.nl](https://mijn.ithodaalderop.nl)

This library is not affiliated with Itho Daalderop or Spider and retrieves date from the endpoints of the mobile application. Use at your own risk.

You will need the gateway in order to communicate. If Itho Daalderop ever takes the cloud environment offline, this library will no longer function. If you are looking for a way to control your fan, I would suggest to use [IthoWifi](https://github.com/arjenhiemstra/ithowifi) as it supports local control.

*Warning: Itho Daalderop is phasing out Spider. Please read [this](https://www.ithodaalderop.nl/additionelespiderproducten) for more information*

## Currently supports

**Thermostat**
- Viewing the current and target temperature
- Changing operation mode to Heat or Cool
- Changing the fan speed

**Power Plugs**
- Viewing the energy usage and the state of power plugs
- Enabling or disabling power plug

## Home Assistant
This library is being used in [Home Assistant](https://www.home-assistant.io/components/spider/) as a component.

## Homey
There is also a [Homey integration](https://github.com/lvanderree/com.synplyworks.spider) for Spider available. It however does not use this library.

## More information about Spider (Dutch)
[https://www.ithodaalderop.nl/nl-NL/professional/productoverzicht/a07](https://www.ithodaalderop.nl/nl-NL/professional/productoverzicht/a07)

## Contributors
* [Peter Nijssen](https://github.com/peternijssen)
* [Stefan Oude Vrielink](https://github.com/soudevrielink)
* [Bennert van Wijs](https://github.com/bennert)
