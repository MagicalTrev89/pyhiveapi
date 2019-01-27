"""Hive Weather Module."""
from pyhiveapi.custom_logging import Logger
from pyhiveapi.hive_data import Data


class Weather:
    """Hive Weather Code."""

    def __init__(self):
        self.log = Logger()

    def temperature(self):
        """Get Hive Weather temperature."""
        self.log.log('Weather', 'Temp', "Gettin outside temp.")
        return Data.w_temperature_value