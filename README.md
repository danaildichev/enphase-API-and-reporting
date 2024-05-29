# enphase-API-and-reporting

![Static Badge](https://img.shields.io/badge/version-1-red)

A Python CLI tool to get data from Enphase API and accompanying dashboard for reporting.

UNDER CONSTRUCTION

## Table of Contents

- [Live Demo](#live-demo)
- [Install](#install)
- [Usage](#usage)
- [API](#api)
- [Issues](#issues)
- [Contributing](#contributing)
- [To Do](#to-do)
- [License](#license)

## Live Demo
Coming soon.

## Install
Coming soon.

## Usage

- You will need an Enphase API dev account and a registered app.
- See the [Enphase API "Quick Start"](https://developer-v4.enphase.com/docs/quickstart.html)

### MVP
See script/mvp for an example of how to call the Enphase API. Requires a valid access token.

### Version 1

Assuming you have a valid access token, the simplest way to print a response from Enphase is to call

```python
from utils.Enphase import Enphase
# initialize with json configs
enphase = Enphase(APP, API, AUTH, SYS, is_verbose=True)
enphase.try_to_get("systems") # https://api.enphaseenergy.com/api/v4/systems
```

With the `EnphaseEndpointLibrary` class, you can call the `record_response()` function to record responses as JSON to the 'response_logs' folder.

```python
from utils.Enphase import Enphase
from utils.EnphaseEndpointLibrary import EnphaseEndpointLibrary
from utils.FileWriter import FileWriter
from utils.JsonCopier import JsonCopier

# initialize JSON configs

enphase = Enphase(_APP, _API, _AUTH, _SYS, is_verbose=True)
file_writer = FileWriter('./response_logs/')
enphase_api = EnphaseEndpointLibrary(enphase, file_writer)

enphase_api.record_response('systems.json', 'systems') # https://api.enphaseenergy.com/api/v4/systems
```

## API

Additional descriptions for using modules in version 1 coming soon.

## Issues

Open an issue or hit me up.

## Contributing

PRs accepted.

## To Do

1. Build a Reporting Module for turning responses into formatted JSON for the web UI.
2. Build the web UI.

## License

MIT
