import json

from . import apifunction, serializer
from . import computedobject
from . import oge_exception
from . import element
from . import coverage
from . import http_util
import copy


class CoverageArray(element.Element):
    """Representation for an Earth Engine ImageCollection."""

    _initialized = False

    def __init__(self, args):
        """CoverageArray constructor."""

        self.initialize()

        # Wrap single images in an array.
        if isinstance(args, dict):
            keys_to_extract = set(['baseUrl', 'productID', 'datetime', 'bbox', 'bboxCrs', 'cloudCoverMin','cloudCoverMax'])
            request = {}
            params = {}
            if args:
                for key in args:
                    if key in keys_to_extract:
                        params[key] = args[key]
                    else:
                        request[key] = args[key]
            super(CoverageArray, self).__init__(apifunction.ApiFunction.lookup('Service.getCoverageArray'), params)
        elif isinstance(args, computedobject.ComputedObject):
            # A custom object to reinterpret as an ImageCollection.
            super(CoverageArray, self).__init__(args.func, args.args, args.varName)
        else:
            raise oge_exception.OGException(
                'Unrecognized argument type to convert to an ImageCollection: %s' %
                args)

    @classmethod
    def initialize(cls):
        """Imports API functions to this class."""
        if not cls._initialized:
            super(CoverageArray, cls).initialize()
            apifunction.ApiFunction.importApi(
                cls, 'CoverageArray', 'CoverageArray')
            cls._initialized = True

    @classmethod
    def reset(cls):
        """Removes imported API functions from this class."""
        apifunction.ApiFunction.clearApi(cls)
        cls._initialized = False

    @staticmethod
    def name():
        return 'CoverageArray'

    @staticmethod
    def elementType():
        return coverage.Coverage

    def styles(self, params=None):
        if params is None:
            return self
        else:
            keys_to_extract = {'bands', 'gain', 'bias', 'min', 'max', 'gamma', 'palette', 'opacity', 'format', 'method'}
            request = {}
            vis_params = {}
            if params:
                for key in params:
                    if key in keys_to_extract:
                        vis_params[key] = params[key]
                    else:
                        request[key] = params[key]
            vis_params['coverageArray'] = self
            return apifunction.ApiFunction.apply_('CoverageArray.addStyles', vis_params)

    def export(self, params):
        keys_to_extract = set(['description', 'crs', 'scale', 'folder', 'fileName', 'fileFormat'])
        export_params = {}
        if params:
            for key in params:
                if key in keys_to_extract:
                    export_params[key] = params[key]
        coverageArray = self
        dag_export_params = copy.deepcopy(export_params)
        dag_export_params['coverageArray'] = coverageArray
        coverageArray = apifunction.ApiFunction.apply_('CoverageArray.export', dag_export_params)

        dag_json = json.dumps(serializer.encode(coverageArray, for_cloud_api=True)["values"])
        http_util.HTTPUtil.batchDagJson(dag_json, export_params)

    # def getMap(self):
    #     dagJson = json.dumps(serializer.encode(self, for_cloud_api=True)["values"])
    #     http_util.HTTPUtil.postDagJson(dagJson)
    #     # print(DAGJson)
    #     # return serializer.encode(self, for_cloud_api=True)["values"]

    def map(self, algorithm, opt_dropNulls=None):
        """Maps an algorithm over an Array."""
        element_type = self.elementType()
        with_cast = lambda e: algorithm(element_type(e))
        return self._cast(apifunction.ApiFunction.call_(
            'Collection.map', self, with_cast, opt_dropNulls))
