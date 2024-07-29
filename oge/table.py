from . import element
from . import apifunction
from . import oge_types
from . import oge_exception
from . import computedobject
from . import serializer
import json
from . import  http_util


class Table(element.Element):
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
                super(Table, self).__init__(
                    apifunction.ApiFunction.lookup('Coverage.load'),
                    {'id': args, 'version': version})
            else:
                raise oge_exception.OGException(
                    'If version is specified, the arg to Image() must be a string. '
                    'Received: %s' % (args,))
            return

        # 这里增加判断是否是字典类型，由字典类型创建Image
        if isinstance(args, dict) and (args.__contains__("baseUrl") is not True):
            keys_to_extract = set(['productID'])
            request = {}
            image_params = {}
            if args:
                for key in args:
                    if key in keys_to_extract:
                        image_params[key] = args[key]
                    else:
                        request[key] = args[key]
            super(Table, self).__init__(
                apifunction.ApiFunction.lookup('Table.load'), image_params)
        elif isinstance(args, dict) and args.__contains__("baseUrl"):
            keys_to_extract = set(['baseUrl', 'productID'])
            request = {}
            table_params = {}
            if args:
                for key in args:
                    if key in keys_to_extract:
                        table_params[key] = args[key]
                    else:
                        request[key] = args[key]
            super(Table, self).__init__(
                apifunction.ApiFunction.lookup('Service.getTable'), table_params)
        elif isinstance(args, computedobject.ComputedObject):
            # A custom object to reinterpret as an Image.
            super(Table, self).__init__(args.func, args.args, args.varName)
        elif oge_types.isString(args):
            super(Table, self).__init__(
                apifunction.ApiFunction.lookup('Table.load'), args)
        # elif args is None:
        #     super(Coverage, self).__init__(
        #         apifunction.ApiFunction.lookup('Image.mask'),
        #         {'image': Coverage(0), 'mask': Coverage(0)})
        else:
            raise oge_exception.OGException(
                'Unrecognized argument type to convert to an Image: %s' % args)

    # @staticmethod
    # def process(process_id):
    #     api_function = ApiFunction.lookup(process_id)
    #     return process.Process(api_function)



    @classmethod
    def initialize(cls, url="http://localhost"):
        """Imports API functions to this class."""
        if not cls._initialized:
            apifunction.ApiFunction.importApi(cls, 'Coverage', 'Coverage')
            cls._initialized = True

    @classmethod
    def getUrl(cls):
        return cls._url

    @staticmethod
    def name():
        return 'Table'

    def getDownLoadUrl(self, format, name):
        url = apifunction.ApiFunction.lookup('Table.getDownloadUrl').call(self, format, name)
        dagJson = json.dumps(serializer.encode(url, for_cloud_api=True)["values"])
        http_util.HTTPUtil.postDagJson(dagJson)
        # print(dagJson)

    def getMap(self):
        print(1)
        visualizeObject =  url = apifunction.ApiFunction.lookup('Table.addStyles').call(self)
        dagJson = json.dumps(serializer.encode(visualizeObject, for_cloud_api=True)["values"])
        http_util.HTTPUtil.postDagJson(dagJson)