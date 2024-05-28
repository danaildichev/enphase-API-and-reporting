from time import sleep


class EnphaseEndpointLibrary:

    def __init__(self, enphase, file_writer):
        """
        Contains functions to call and record the 'gettable' Enphase endpoints.

        Parameters:
            enphase (Enphase): An instance of utils.Enphase
            file_writer (FileWriter): An instance of utils.FileWriter
        """
        self.enphase = enphase
        self.file_writer = file_writer

        # store common substrings found in API docs
        self.prefix = {
            'systems': f"systems/{self.enphase.system_id}"
        }

        # store common params for lifetime endpoints
        self.lifetime_pairs = {

            'energy': {
                'filename': 'energy_lifetime.json',
                'endpoint': 'energy_lifetime'
            },

            'consumption': {
                'filename': 'consumption_lifetime.json',
                'endpoint': 'consumption_lifetime'
            },

            'battery': {
                'filename': 'battery_lifetime.json',
                'endpoint': 'battery_lifetime'
            },

            'energy_import': {
                'filename': 'energy_import_lifetime.json',
                'endpoint': 'energy_import_lifetime'
            },

            'energy_export': {
                'filename': 'energy_export_lifetime.json',
                'endpoint': 'energy_export_lifetime'
            }
        }

    # end __init__()

    def record_response(self, file_name, endpoint, params=None, custom_headers=None):
        """
        Handles try/except block of getting a response from Enphse API.
        Then records the response text as the specified file name.

        Parameters:
            endpoint (str): anything after '/api/v4/' in the Enphase API docs
            params (dict): URL params for the request
            custom_headers (dict): Overwrite for default request header. Unlikely to be needed.
            file_name (str): What file name or path the recorded response should be saved as.
        """
        response = self.enphase.try_to_get_response(endpoint, params, custom_headers)
        self.file_writer.create(file_name, response.text)
    # end record_response()

    def systems(self, file_name, endpoint, params=None, custom_headers=None):
        """ Use self.record_response() with the default systems prefix """
        self.record_response(file_name, f"{self.prefix['systems']}/{endpoint}", params, custom_headers)
    # end systems()

    def lifetime(self, key, params=None, custom_headers=None):
        """ Use self.systems() with predefined filenames and endpoints in self.lifetime_params """
        file_name = self.lifetime_pairs[key]['filename']
        endpoint = self.lifetime_pairs[key]['endpoint']
        self.systems(file_name, endpoint, params, custom_headers)
    # end lifetime()

    def get_lifetime_data_for(self, pairs):
        """
        Uses self.lifetime() to get and record multiple responses from Enphase.
        Requests are delayed based on rate limit per API subscription tier.

        Parameters:
            pairs (list): Can include 'energy', 'consumption', 'battery', 'energy_import', 'energy_export'

        """
        for i in range(len(pairs)):
            self.lifetime(pairs[i])
            if i < len(pairs) - 1:
                sleep(self.enphase.request_delay)
    # end get_lifetime_data_for()

    # def energy_lifetime(self, params=None, custom_headers=None):
    #     """ /api/v4/systems/{system_id}/energy_lifetime """
    #     self.systems('energy_lifetime.json', "energy_lifetime", params, custom_headers)
    # end energy_lifetime()

    # def consumption_lifetime(self, params=None, custom_headers=None):
    #     """ /api/v4/systems/{system_id}/consumption_lifetime """
    #     self.systems('consumption_lifetime.json', "consumption_lifetime", params, custom_headers)
    # end consumption_lifetime()

    # def battery_lifetime(self, params=None, custom_headers=None):
    #     """ /api/v4/systems/{system_id}/battery_lifetime """
    #     self.systems('battery_lifetime.json', "battery_lifetime", params, custom_headers)
    # end battery_lifetime()

    # def energy_import_lifetime(self, params=None, custom_headers=None):
    #     """ /api/v4/systems/{system_id}/energy_import_lifetime """
    #     self.systems('energy_import_lifetime.json', "energy_import_lifetime", params, custom_headers)
    # end energy_import_lifetime()

    # def energy_export_lifetime(self, params=None, custom_headers=None):
    #     """ /api/v4/systems/{system_id}/energy_export_lifetime """
    #     self.systems('energy_export_lifetime.json', "energy_export_lifetime", params, custom_headers)
    # end energy_export_lifetime()



