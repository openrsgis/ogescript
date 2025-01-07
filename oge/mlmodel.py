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
        elif isinstance(args, dict) and args.__contains__("baseUrl"):
            keys_to_extract = set(['baseUrl', 'modelID'])
            request = {}
            coverage_params = {}
            if args:
                for key in args:
                    if key in keys_to_extract:
                        coverage_params[key] = args[key]
                    else:
                        request[key] = args[key]
            super(MLmodel, self).__init__(
                apifunction.ApiFunction.lookup('Service.getModel'), coverage_params)
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

    def export(self, params):
        keys_to_extract = set(['taskName', 'fileName'])
        export_params = {}
        if params:
            for key in params:
                if key in keys_to_extract:
                    export_params[key] = params[key]
        mlmodel = self
        dag_export_params = copy.deepcopy(export_params)
        dag_export_params['model'] = mlmodel
        mlmodel = apifunction.ApiFunction.apply_('MLmodel.export', dag_export_params)
        dag_json = json.dumps(serializer.encode(mlmodel, for_cloud_api=True)["values"])
        http_util.HTTPUtil.batchDagJson(dag_json, export_params)
        return


