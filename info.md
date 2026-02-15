# Fritz Advanced Thermostat Offset

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

### Parameters

| Key | Required | Type | Default | Description |
|-----|----------|------|---------|-------------|
| `module` | Yes | string | | Must be `fritz_thermostat_offset` |
| `class` | Yes | string | | Must be `FritzThermostatOffset` |
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
| `thermostat` | Yes | string or list | Fritz!Box thermostat name(s) |
| `thermometer` | Yes | string | Home Assistant temperature sensor entity_id |

Use a list for `thermostat` when multiple thermostats share a room with one external sensor.
