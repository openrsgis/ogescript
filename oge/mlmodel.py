import json

from . import oge_exception, serializer
from . import oge_types
from . import element
from . import apifunction
from . import computedobject
from . import data
from . import http_util
import copy


class MLmodel(element.Element):
    _initialized = False

    def __init__(self, args = None):
        self.initialize()

        if isinstance(args, computedobject.ComputedObject):
            # A custom object to reinterpret as an MLmodel.
            super(MLmodel, self).__init__(args.func, args.args, args.varName)
        else:
            raise oge_exception.OGException(
                'Unrecognized argument type to convert to an MLmodel: %s' % args)

    @classmethod
    def initialize(cls):
        """Imports API functions to this class."""
        if not cls._initialized:
            apifunction.ApiFunction.importApi(cls, 'MLmodel', 'MLmodel')
            cls._initialized = True

    @staticmethod
    def name():
        return 'MLmodel'

    @classmethod
    def reset(cls):
        """Removes imported API functions from this class."""
        apifunction.ApiFunction.clearApi(cls)
        cls._initialized = False


