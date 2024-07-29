import json

from . import apifunction, serializer
from . import computedobject
from . import data
from . import oge_exception
from . import oge_types
from . import element
from . import http_util
import copy


class Coverage(element.Element):
    _initialized = False

    def __init__(self, args=None, version=None):
        """Constructs an Earth Engine image.

    Args:
      args: This constructor accepts a variety of arguments:
          - A string - an EarthEngine asset id,
          - A string and a number - an EarthEngine asset id and version,
          - A number - creates a constant image,
          - An ee.Array - creates a constant array image,
          - A list - creates an image out of each element of the array and
            combines them into a single image,
          - An ee.Image - returns the argument,
          - Nothing - results in an empty transparent image.
      version: An optional asset version.

    Raises:
      OGException: if passed something other than the above.
    """

        self.initialize()

        if version is not None:
            if oge_types.isString(args) and oge_types.isNumber(version):
                # An ID and version.
                super(Coverage, self).__init__(
                    apifunction.ApiFunction.lookup('Coverage.load'),
                    {'id': args, 'version': version})
            else:
                raise oge_exception.OGException(
                    'If version is specified, the arg to Image() must be a string. '
                    'Received: %s' % (args,))
            return

        # 这里增加判断是否是字典类型，由字典类型创建Image
        if isinstance(args, dict) and (args.__contains__("baseUrl") is not True):
            keys_to_extract = set(['productName', 'sensorName', 'measurementName', 'StartTime', 'EndTime', 'geom', 'crs', 'method'])
            request = {}
            image_params = {}
            if args:
                for key in args:
                    if key in keys_to_extract:
                        image_params[key] = args[key]
                    else:
                        request[key] = args[key]
            super(Coverage, self).__init__(
                apifunction.ApiFunction.lookup('Coverage.load'), image_params)
        elif isinstance(args, dict) and args.__contains__("baseUrl"):
            keys_to_extract = set(['baseUrl', 'productID', 'coverageID', 'subset', 'properties'])
            request = {}
            coverage_params = {}
            if args:
                for key in args:
                    if key in keys_to_extract:
                        coverage_params[key] = args[key]
                    else:
                        request[key] = args[key]
            super(Coverage, self).__init__(
                apifunction.ApiFunction.lookup('Service.getCoverage'), coverage_params)
        elif isinstance(args, computedobject.ComputedObject):
            # A custom object to reinterpret as an Image.
            super(Coverage, self).__init__(args.func, args.args, args.varName)
        # elif args is None:
        #     super(Coverage, self).__init__(
        #         apifunction.ApiFunction.lookup('Image.mask'),
        #         {'image': Coverage(0), 'mask': Coverage(0)})
        else:
            raise oge_exception.OGException(
                'Unrecognized argument type to convert to an Image: %s' % args)

    @classmethod
    def initialize(cls):
        """Imports API functions to this class."""
        if not cls._initialized:
            apifunction.ApiFunction.importApi(cls, 'Coverage', 'Coverage')
            cls._initialized = True

    def getMapId(self, vis_params=None):
        """Fetch and return a map ID dictionary, suitable for use in a Map overlay.

        Args:
          vis_params: The visualization parameters.  See ee.data.getMapId.

        Returns:
          A map ID dictionary as described in ee.data.getMapId.
        """
        vis_image, request = self._apply_visualization(vis_params)
        request['image'] = vis_image
        response = data.getMapId(request)
        response['Coverage'] = self
        return response

    def _apply_visualization(self, params):
        """Applies visualization parameters to an image.

        Wraps the image in a call to visualize() if there are any recognized
        visualization parameters present.

        Args:
          params: the request parameters.

        Returns:
          A tuple containing:
          - the result of applying the visualization parameters to this image
          - any remaining (non-visualization) parameters.
        """
        # Split the parameters into those handled handled by visualize()
        # and those that aren't.
        keys_to_extract = {'bands', 'gain', 'bias', 'min', 'max', 'gamma', 'palette', 'opacity', 'format'}
        request = {}
        vis_params = {}
        if params:
            for key in params:
                if key in keys_to_extract:
                    vis_params[key] = params[key]
                else:
                    request[key] = params[key]
        coverage = self
        # GEE中如果可视化是有输入参数的，那么需要调用Image.visualize算子；如果没有，就不需要调用该算子，这里修改不用参数同样调用visualize算子
        if vis_params:
            vis_params['coverage'] = coverage
            coverage = apifunction.ApiFunction.apply_('Coverage.visualize', vis_params)
        # vis_params['Coverage'] = image
        # image = apifunction.ApiFunction.apply_('Coverage.visualize', vis_params)
        return coverage, request

    @staticmethod
    def name():
        return 'Coverage'

    def styles(self, params=None):
        if params is None:
            return self
        else:
            keys_to_extract = {'bands', 'gain', 'bias', 'min', 'max', 'gamma', 'palette', 'opacity', 'format'}
            request = {}
            vis_params = {}
            if params:
                for key in params:
                    if key in keys_to_extract:
                        vis_params[key] = params[key]
                    else:
                        request[key] = params[key]
            coverage = self
            vis_params['coverage'] = coverage
            coverage = apifunction.ApiFunction.apply_('Coverage.addStyles', vis_params)
            return coverage

    def export(self, params):
        keys_to_extract = set(['description', 'crs', 'scale', 'folder', 'fileName', 'fileFormat'])
        export_params = {}
        if params:
            for key in params:
                if key in keys_to_extract:
                    export_params[key] = params[key]
        coverage = self
        dag_export_params = copy.deepcopy(export_params)
        dag_export_params['coverage'] = coverage
        coverage = apifunction.ApiFunction.apply_('Coverage.export', dag_export_params)

        dag_json = json.dumps(serializer.encode(coverage, for_cloud_api=True)["values"])
        http_util.HTTPUtil.batchDagJson(dag_json, export_params)

    # def getMap(self):
    #     dagJson = json.dumps(serializer.encode(self, for_cloud_api=True)["values"])
    #     http_util.HTTPUtil.postDagJson(dagJson)
        # print(DAGJson)
