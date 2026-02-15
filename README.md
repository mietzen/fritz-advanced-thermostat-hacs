# Fritz Advanced Thermostat Offset

An [AppDaemon](https://appdaemon.readthedocs.io/) app for [HACS](https://hacs.xyz/) that automatically adjusts Fritz!DECT thermostat temperature offsets based on external Home Assistant temperature sensors.

Uses [fritz-advanced-thermostat](https://github.com/mietzen/python-fritz-advanced-thermostat) to communicate with the Fritz!Box via its undocumented web API.

## How It Works

Fritz!DECT thermostats have a built-in temperature sensor that can be inaccurate due to placement (e.g. near a radiator). This app periodically:

1. Reads the actual room temperature from an external HA sensor
2. Reads the thermostat's current temperature and offset from the Fritz!Box
3. Calculates and applies a new offset so the thermostat matches the actual temperature

## Installation

### HACS

1. Add this repository as a custom repository in HACS (category: AppDaemon)
2. Install "Fritz Advanced Thermostat Offset"
3. Add the configuration to your `apps.yaml`

### Manual

Download the `fritz_thermostat_offset` directory from `apps/` to your local AppDaemon `apps` directory.

## Requirements

Add the following to your AppDaemon `requirements.txt` (or the packages section in your addon config):

```txt
fritz-advanced-thermostat
```

You will also need to [set up a Fritz!Box user](https://github.com/hthiery/python-fritzhome#fritzbox-user) with smart home permissions.

## Configuration

Add the following to your `apps.yaml`:

```yaml
fritz_thermostat_offset:
  module: fritz_thermostat_offset
  class: FritzThermostatOffset
  fritz_host: !secret fritz_host
  fritz_user: !secret fritz_user
  fritz_password: !secret fritz_password
  interval: 300
  thermostats:
    - thermostat: kitchen
      thermometer: sensor.kitchen_thermo_temperature
    - thermostat:
        - livingroom_north
        - livingroom_west
      thermometer: sensor.livingroom_thermo_temperature
```

And add the secrets to your `secrets.yaml`:

```yaml
fritz_host: "192.168.178.1"
fritz_user: "my-user"
fritz_password: "my-password"
```

### Parameters

| Key | Required | Type | Default | Description |
|-----|----------|------|---------|-------------|
| `fritz_host` | Yes | string | | Fritz!Box IP or hostname |
| `fritz_user` | Yes | string | | Fritz!Box username |
| `fritz_password` | Yes | string | | Fritz!Box password |
| `ssl_verify` | No | bool | `false` | Verify SSL certificate |
| `interval` | No | int | `300` | Polling interval in seconds |
| `max_offset` | No | float | `5.0` | Maximum allowed offset |
| `min_offset` | No | float | `-5.0` | Minimum allowed offset |
| `thermostats` | Yes | list | | List of thermostat-to-sensor mappings |

### Thermostat Mapping

Each entry in `thermostats` maps one or more Fritz!Box thermostats to a Home Assistant temperature sensor:

| Key | Required | Type | Description |
|-----|----------|------|-------------|
| `thermostat` | Yes | string or list | Fritz!Box thermostat name(s) as shown in the Fritz!Box UI |
| `thermometer` | Yes | string | Home Assistant temperature sensor entity_id |

Use a list for `thermostat` when multiple thermostats share a room with one external sensor.

## Disclaimer

**This package is not related to or developed by AVM. No relationship between the developer of this package and AVM exists.**

**All trademarks, logos and brand names are the property of their respective owners. All company, product and service names used in this package are for identification purposes only. Use of these names, trademarks and brands does not imply endorsement.**
