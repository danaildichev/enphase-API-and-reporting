from math import ceil
import requests
from datetime import datetime


class Enphase:

    def __init__(self, config_app, config_api, config_auth, system_details, is_verbose=False):
        """
        Sets instance variables for use in this class.

        Parameters:
            config_app (json) from file config.json
            config_api (json) from file config.json
            config_auth (json) from file OAuth2.json
            system_details (json) from file system.json
            is_verbose (bool) optional. default is false. whether instance should be chatty.
        """
        # flag for self.verbose()
        self.is_verbose = is_verbose

        # store details from configs
        self._APP = config_app
        self._API = config_api
        self._AUTH = config_auth
        self._SYS = system_details

        # get pertinent details from configs
        self.api = {
            'url': f"{self._API['ROOT']}{self._API['BASE']}",
            'key': self._APP['API_KEY']
        }

        # OAuth tokens
        self.tokens = {
            'bearer': self._AUTH['access_token'],
            'refresh': self._AUTH['refresh_token']
        }

        # app id was assigned to dev by creating an Enphase API account
        self.app_id = self._AUTH['app_Id']

        # the home-owner whose account this app is using has one 'system'
        # device ids and serial numbers have been pulled from the Enphase API
        self.system_meta = self._SYS['meta']
        self.system_start_timestamp = self.system_meta['operational_at']
        self.system_start_date = datetime.fromtimestamp(self.system_start_timestamp).strftime('%Y-%m-%d')
        self.system_id = self._SYS['meta']['id']
        self.system_micros = self._SYS['devices']['micros']
        self.system_meters = self._SYS['devices']['meters']
        self.system_gateway = self._SYS['devices']['gateway']
        self.request_delay = ceil(60 / self._APP['RATE_LIMIT'])

    # end __init__()

    def verbose(self, message):
        """ Print a message to the terminal if class instance is verbose """
        if self.is_verbose:
            print(message)
    # end verbose()

    def default_path(self, endpoint):
        """
        Get the default path to an endpoint

        Parameters:
            endpoint (str): the endpoint to be used in generating the path. e.g. 'systems'

        Returns:
            (str): the endpoint URL. e.g. 'https://api.enphaseenergy.com/api/v4/systems'

        """
        return f"{self.api['url']}{endpoint}"
    # end default_path()

    def default_headers(self):
        """
        Get the default headers for making a request.

        Returns:
              (dict): 'Authorization' with 'bearer token' from OAuth2.json and 'key' with 'API_KEY' from config.json
        """
        return {
            'Authorization': f"Bearer {self.tokens['bearer']}",
            'key': self.api['key']
        }
    # end get_default_headers()

    def send_get_request(self, endpoint, params=None, custom_headers=None):
        """
        Perform a GET request to the Enphase API.
        See https://requests.readthedocs.io/en/latest/api/#requests.get

        Parameters:
            endpoint (str): which endpoint to use. e.g. 'systems/{system_id}'
            params (dict): optional URL params. default is None
            custom_headers (dict): optional headers for GET request. default is None, meaning call will be made using self.default_headers()

        Returns:
            (Response): The server's response to the GET request.
            See https://requests.readthedocs.io/en/latest/api/#requests.Response
        """
        path = self.default_path(endpoint)
        head = custom_headers or self.default_headers()

        # if verbose, print to terminal
        self.verbose(f"Making GET request to {path}")
        if params:
            self.verbose(f"Using params {params}")
        if custom_headers:
            self.verbose(f"Using custom headers {custom_headers}")
        # end if verbose, print to terminal

        return requests.get(path, params, headers=head)
    # end get()

    def print_reminder_for_renewing_oauth_tokens(self):
        """ Suggests what user should do if GET request is denied with 401 Unauthorized """
        print('\nRefer to Enphase API Quickstart for renewing OAuth access.')
        print('https://developer-v4.enphase.com/docs/quickstart.html')
        print('If it has been less than 30 days since the OAuth2.json file was last updated, see step 10 for renewing an access token.')
        print('Otherwise the refresh token is expired. Dev and home-owner will have to perform steps 3 through 8.')
        print('\n\nConsider running "legacy_get_refreshed_access_token.py".')
        print('\n\nNOTE: You may be unauthorized because the info you requested is not available on the current subscription plan.')

        # todo: improve this function
        # - display last-modified time from OAuth2.json file
        # - ask user if they want to run "legacy_get_refreshed_access_token.py"
        #     -- handle failure for legacy refresh script
        #     -- auto update contents of OAuth2.json
        # - if update is successful, ask user if they want to re-run the operation
        # - legacy refresh script could be re-written into Enphase class
    # end print_reminder_for_renewing_OAuth_tokens()

    def try_to_get_response(self, endpoint, params=None, custom_headers=None):
        """ Use self.send_get_request() in a try/except block """
        try:
            response = self.send_get_request(endpoint, params, custom_headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as error:
            # todo: expand exception structure to handle individual exception types
            print('An error occurred while handling the request:')
            print(error)
        else:
            return response
        finally:
            self.verbose(f"Response status: {response.status_code}")
            self.verbose("Response is: \n")
            self.verbose(response.text)

            # unauthorized requests probably just need a new access token
            if response.status_code == 401:
                self.print_reminder_for_renewing_oauth_tokens()
    # end try_to_get()
