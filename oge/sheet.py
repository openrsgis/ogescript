import json

from . import apifunction, serializer
from . import computedobject
from . import data
from . import oge_exception
from . import oge_types
from . import element
from . import http_util
import copy


class Sheet(computedobject.ComputedObject):
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

        # if version is not None:
        #     if oge_types.isString(args) and oge_types.isNumber(version):
        #         # An ID and version.
        #         super(Coverage, self).__init__(
        #             apifunction.ApiFunction.lookup('Coverage.load'),
        #             {'id': args, 'version': version})
        #     else:
        #         raise oge_exception.OGException(
        #             'If version is specified, the arg to Image() must be a string. '
        #             'Received: %s' % (args,))
        #     return

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
            keys_to_extract = set(['baseUrl', 'sheetID'])
            request = {}
            coverage_params = {}
            if args:
                for key in args:
                    if key in keys_to_extract:
                        coverage_params[key] = args[key]
                    else:
                        request[key] = args[key]
            super(Sheet, self).__init__(
                apifunction.ApiFunction.lookup('Service.getSheet'), coverage_params)
        elif isinstance(args, computedobject.ComputedObject):
            # A custom object to reinterpret as an Image.
            super(Sheet, self).__init__(args.func, args.args, args.varName)
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
            apifunction.ApiFunction.importApi(cls, 'Sheet', 'Sheet')
            cls._initialized = True

    @staticmethod
    def name():
        return 'Sheet'

    def log(self,name):
        param = {}
        param['object'] = self
        param["name"] = name
        self = apifunction.ApiFunction.apply_('Service.printSheet',param)
        dag_json = json.dumps(serializer.encode(self,for_cloud_api=True)["values"])
        http_util.HTTPUtil.postDagJson(dag_json, name)

