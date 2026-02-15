"""AppDaemon app to automatically adjust Fritz!DECT thermostat offsets based on external temperature sensors."""

import appdaemon.plugins.hass.hassapi as hass
from fritz_advanced_thermostat import FritzAdvancedThermostat, FritzAdvancedThermostatError


class FritzThermostatOffset(hass.Hass):
    """Adjust Fritz!DECT thermostat offsets using external HA temperature sensors."""

    def initialize(self):
        """Initialize the app: connect to Fritz!Box and start polling."""
        self.fritz_host = self.args["fritz_host"]
        self.fritz_user = self.args["fritz_user"]
        self.fritz_password = self.args["fritz_password"]
        self.ssl_verify = self.args.get("ssl_verify", False)
        self.interval = self.args.get("interval", 300)
        self.max_offset = 5.0
        self.min_offset = -5.0

        self.mappings = self.args["thermostats"]

        self.fat = None

        self.run_every(self.update_offsets, "immediate", self.interval)

    def _connect(self):
        """Create a new Fritz!Box connection."""
        try:
            self.fat = FritzAdvancedThermostat(
                host=self.fritz_host,
                user=self.fritz_user,
                password=self.fritz_password,
                ssl_verify=self.ssl_verify,
            )
            return True
        except FritzAdvancedThermostatError:
            self.log("Failed to connect to Fritz!Box at %s", self.fritz_host, level="ERROR")
            self.fat = None
            return False

    def update_offsets(self, kwargs):
        """Poll all thermostats and adjust offsets based on external sensors."""
        if self.fat is None and not self._connect():
            return

        # Get latest thermostat data
        self.fat.reload_thermostat_data()

        changed = False

        for mapping in self.mappings:
            thermostat_names = mapping["thermostat"]
            if isinstance(thermostat_names, str):
                thermostat_names = [thermostat_names]
            thermometer = mapping["thermometer"]

            actual_temp = self._get_sensor_temperature(thermometer)
            if actual_temp is None:
                continue

            for name in thermostat_names:
                try:
                    thermostat_temp = self.fat.get_thermostat_temperature(name)
                    current_offset = self.fat.get_thermostat_offset(name)

                    new_offset = current_offset + (actual_temp - thermostat_temp)
                    new_offset = round(new_offset * 2) / 2  # Round to 0.5 steps
                    new_offset = max(self.min_offset, min(self.max_offset, new_offset))

                    if new_offset != current_offset:
                        self.log(
                            "%s: actual=%.1f, thermostat=%.1f, offset %.1f -> %.1f",
                            name, actual_temp, thermostat_temp, current_offset, new_offset,
                        )
                        self.fat.set_thermostat_offset(name, new_offset)
                        changed = True
                    else:
                        self.log(
                            "%s: offset %.1f is correct (actual=%.1f, thermostat=%.1f)",
                            name, current_offset, actual_temp, thermostat_temp, level="DEBUG",
                        )
                except FritzAdvancedThermostatError:
                    self.log("Failed to update offset for %s", name, level="ERROR")
                    self.fat = None
                    return

        if changed:
            try:
                self.fat.commit()
                self.log("Committed offset changes to Fritz!Box")
            except FritzAdvancedThermostatError:
                self.log("Failed to commit changes to Fritz!Box", level="ERROR")
                self.fat = None

    def _get_sensor_temperature(self, entity_id):
        """Read temperature from a Home Assistant sensor entity."""
        state = self.get_state(entity_id)
        if state in (None, "unknown", "unavailable"):
            self.log("Sensor %s is unavailable", entity_id, level="WARNING")
            return None
        try:
            return float(state)
        except ValueError:
            self.log("Sensor %s has non-numeric state: %s", entity_id, state, level="WARNING")
            return None
