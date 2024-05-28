from utils.Enphase import Enphase
from utils.EnphaseEndpointLibrary import EnphaseEndpointLibrary
from utils.FileWriter import FileWriter
from utils.JsonCopier import JsonCopier


# -------------------------------------------------------
# load details from config, OAuth2, and system JSON files

# init an object to pull contents from JSON files
json_copy = JsonCopier()

# load details assigned to this app's dev account
config = json_copy.extract_from_file('json/config.json')
_APP = json_copy.deep_constant(config['APP'])
_API = json_copy.deep_constant(config['API'])

# load the most recent OAuth tokens obtained from Enphase API
auth_tokens = json_copy.extract_from_file('json/OAuth2.json')
_AUTH = json_copy.deep_constant(auth_tokens)

# load system details obtained from Enphase API
system_details = json_copy.extract_from_file('json/system.json')
_SYS = json_copy.deep_constant(system_details)

# end load details from config, OAuth2, and system JSON files
# -----------------------------------------------------------

# ------------------------------------------
# init objects to interact with Enphase data

enphase = Enphase(_APP, _API, _AUTH, _SYS, is_verbose=True)
file_writer = FileWriter('./response_logs/')
enphase_api = EnphaseEndpointLibrary(enphase, file_writer)

# end init objects to interact with Enphase data
# ----------------------------------------------


# ====
# main

# Available keys for use with lifetime() are: energy, consumption, battery, energy_import, energy_export
# The system we are using does not have a battery.
# The API subscription we have is rate limited to 10 hits per minute.
enphase_api.get_lifetime_data_for(['energy', 'consumption', 'energy_import', 'energy_export'])

# end main
# ========