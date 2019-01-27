"""Custom Logging Module."""
import os
from datetime import datetime

from pyhiveapi.hive_data import Data


class Logger:
    """Custom Logging Code."""

    def __init__(self):
        """Logger Initialisation"""

    @staticmethod
    def check_logging(new_session):
        """Check Logging Active"""
        Data.l_o_folder = os.path.expanduser('~') + "/.homeassistant/pyhiveapi"
        Data.l_o_file = Data.l_o_folder + "/pyhiveapi.log"
        count = 0
        try:
            if new_session and os.path.isfile(Data.l_o_file):
                os.remove(Data.l_o_file)

            if os.path.isdir(Data.l_o_folder):
                for a in Data.l_files:
                    t = Data.l_o_folder + "/" + Data.l_files[a]
                    if os.path.isfile(t):
                        Data.l_values.update({a: True})
                        Data.l_values.update({'enabled': True})
                    elif os.path.isfile(t) is False:
                        count += 1
                        if count == len(Data.l_files):
                            Data.l_values = {}
        except FileNotFoundError:
            Data.l_values = {}

    @staticmethod
    def log(n_id, l_type, new_message, **kwargs):
        """Output new log entry if logging is turned on."""
        name = Data.NAME.get(n_id, n_id)
        data = kwargs.get('info', None)
        if n_id == 'No_ID':
            name = 'Hive'
        f = False
        if '_' in l_type:
            x = l_type.split("_")
            for i in x:
                if i in Data.l_values or 'all' in Data.l_values:
                    if Data.l_values['enabled']:
                        f = True
                        break
        elif l_type in Data.l_values or 'all' in Data.l_values:
            if Data.l_values['enabled']:
                f = True

        if f:
            try:
                l_file = open(Data.l_o_file, "a")
                l_file.write(datetime.now().strftime("%d-%b-%Y %H:%M:%S") +
                             " - " + l_type + "-" + name + " : " +
                             + new_message.format(data) + "\n")
                l_file.close()
            except FileNotFoundError:
                pass
        else:
            pass

    def error_check(self, n_id, n_type, error_type, **kwargs):
        """Error has occurred."""
        import re
        message = None
        new_data = None
        if error_type == 'Offline':
            message = "Offline could not update entity."
        elif error_type == 'Failed:':
            message = "ERROR - No data found for device."
        elif error_type == 'Failed_API':
            code = kwargs.get('resp')
            new_data = re.search('[0-9][0-9][0-9]', code)
            message = "ERROR - Received {0} response from API."
        self.log(n_id, n_type, message, info=new_data)