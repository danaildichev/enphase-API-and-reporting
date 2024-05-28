import copy
import json
from types import MappingProxyType


class JsonCopier:

    def __init__(self):
        pass
    # end __init__()

    def extract_from_file(self, filepath):
        """ Returns contents from 'filepath' as a dict """
        with open(filepath) as contents:
            return json.load(contents)
    # end extract_json_from_file()

    def deep(self, source):
        """ Get a deep copy of contents in 'filepath' """
        return copy.deepcopy(source)
    # end deep()

    def deep_constant(self, source):
        """ Get an immutable deep copy of 'source' """
        return MappingProxyType(self.deep(source))
    # end deep_constant()
