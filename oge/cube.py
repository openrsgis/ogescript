import json

from . import oge_exception, serializer
from . import oge_types
from . import element
from . import apifunction
from . import computedobject
from . import data
from . import http_util
import copy


class Cube(element.Element):
    _initialized = False

    def __init__(self, args=None, version=None):
        self.initialize()

        if version is not None:
            if oge_types.isString(args) and oge_types.isNumber(version):
                # An ID and version.
                super(Cube, self).__init__(
                    apifunction.ApiFunction.lookup('Service.getCube'),
                    {'id': args, 'version': version})
            else:
                raise oge_exception.OGException(
                    'If version is specified, the arg to Image() must be a string. '
                    'Received: %s' % (args,))
            return

        #这里增加判断是否是字典类型，由字典类型创建Cube
        if isinstance(args, dict):
            # 判断是构建还是加载
            if "extent" in args.keys() and 'gridDimX' in args.keys():
                self.build(args)
            else:
                keys_to_extract = set(['cubeId', 'products', 'bands', 'time', 'extent', 'tms', 'resolution'])
                request = {}
                cube_params = {}
                if args:
                    for key in args:
                        if key in keys_to_extract:
                            cube_params[key] = args[key]
                        else:
                            request[key] = args[key]
                super(Cube, self).__init__(
                    apifunction.ApiFunction.lookup('Service.getCube'), cube_params)
        elif isinstance(args, computedobject.ComputedObject):
            if args.name() == 'Array':
                # A constant array image.
                super(Cube, self).__init__(
                    apifunction.ApiFunction.lookup('Image.constant'), {'value': args})
            else:
                # A custom object to reinterpret as an Image.
                super(Cube, self).__init__(args.func, args.args, args.varName)
        else:
            raise oge_exception.OGException(
                'Unrecognized argument type to convert to an Image: %s' % args)

    @classmethod
    def initialize(cls):
        """Imports API functions to this class."""
        if not cls._initialized:
            apifunction.ApiFunction.importApi(cls, 'Cube', 'Cube')
            cls._initialized = True

    @staticmethod
    def name():
        return 'Cube'

    def _apply_visualization(self, params):
        keys_to_extract = set(['bands', 'products', 'gain', 'bias', 'min', 'max',
                               'gamma', 'palette', 'opacity', 'format'])
        request = {}
        vis_params = {}
        if params:
            for key in params:
                if key in keys_to_extract:
                    vis_params[key] = params[key]
                else:
                    request[key] = params[key]
        image = self
        # 如果可视化是有输入参数的，那么需要调用Image.visualize算子；如果没有，就不需要调用该算子，这里修改不用参数同样调用visualize算子
        if vis_params:
            vis_params['cube'] = image
            image = apifunction.ApiFunction.apply_('Cube.visualize', vis_params)
        # vis_params['cube'] = image
        # image = apifunction.ApiFunction.apply_('Cube.visualize', vis_params)
        return image, request

    def getMapId(self, vis_params=None):
        """Fetch and return a map ID dictionary, suitable for use in a Map overlay.

        Args:
          vis_params: The visualization parameters.  See ee.data.getMapId.

        Returns:
          A map ID dictionary as described in ee.data.getMapId.
        """
        vis_image, request = self._apply_visualization(vis_params)
        request['cube'] = vis_image
        response = data.getMapId(request)
        response['cube'] = self
        return response

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
            cube = self
            vis_params['cube'] = cube
            return apifunction.ApiFunction.apply_('Cube.addStyles', vis_params)

    def map(self):
        # DAGJson = serializer.encode(self, for_cloud_api=True)["values"]
        dagJson = json.dumps(serializer.encode(self, for_cloud_api=True)["values"])
        http_util.HTTPUtil.postDagJson(dagJson)
        # print(DAGJson)
        # return serializer.encode(self, for_cloud_api=True)["values"]

    def export(self, params):
        keys_to_extract = {'description', 'crs', 'scale', 'folder', 'fileName', 'fileFormat'}
        export_params = {}
        if params:
            for key in params:
                if key in keys_to_extract:
                    export_params[key] = params[key]
        cube = self
        dag_export_params = copy.deepcopy(export_params)
        dag_export_params['cube'] = cube
        cube = apifunction.ApiFunction.apply_('Cube.export', dag_export_params)

        dag_json = json.dumps(serializer.encode(cube, for_cloud_api=True)["values"])
        http_util.HTTPUtil.batchDagJson(dag_json, export_params)

    def build(self, args):
        # 这里增加判断是否是字典类型，由字典类型构建Cube
        if isinstance(args, dict):
            keys_to_extract = {'productIDList', 'coverageIDList', 'gridDimX', 'gridDimY', 'extents', 'startTime',
                               'endTime'}
            request = {}
            cube_params = {}
            if args:
                for key in args:
                    if key in keys_to_extract:
                        cube_params[key] = args[key]
                    else:
                        request[key] = args[key]
            super(Cube, self).__init__(
                apifunction.ApiFunction.lookup('Cube.build'), cube_params)
        elif isinstance(args, computedobject.ComputedObject):
            if args.name() == 'Array':
                # A constant array image.
                super(Cube, self).__init__(
                    apifunction.ApiFunction.lookup('Image.constant'), {'value': args})
            else:
                # A custom object to reinterpret as an Image.
                super(Cube, self).__init__(args.func, args.args, args.varName)
        else:
            raise oge_exception.OGException(
                'Unrecognized argument type to convert to an Image: %s' % args)
