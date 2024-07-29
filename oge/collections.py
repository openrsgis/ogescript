from . import element
from . import apifunction
from . import computedobject
from . import oge_exception


class Collections(element.Element):
    _initialized = False

    def __init__(self, args=None, version=None):
        self.initialize()
        if isinstance(args, dict):
            keys_to_extract = set(['productIDs', 'baseUrl', 'datetime', 'bbox', 'bboxCrs'])
            request = {}
            collections_params = {}
            if args:
                for key in args:
                    if key in keys_to_extract:
                        collections_params[key] = args[key]
                    else:
                        request[key] = args[key]
            super(Collections, self).__init__(
                apifunction.ApiFunction.lookup('Service.getCollections'), collections_params)
        elif isinstance(args, computedobject.ComputedObject):
            if args.name() == 'Array':
                # A constant array image.
                super(Collections, self).__init__(
                    apifunction.ApiFunction.lookup('Image.constant'), {'value': args})
            else:
                # A custom object to reinterpret as an Image.
                super(Collections, self).__init__(args.func, args.args, args.varName)
        else:
            raise oge_exception.OGException(
                'Unrecognized argument type to convert to an Image: %s' % args)

    @classmethod
    def initialize(cls):
        """Imports API functions to this class."""
        if not cls._initialized:
            apifunction.ApiFunction.importApi(cls, 'Collections', 'Collections')
            cls._initialized = True

    def collection(self, collection_id="", bbox=None, datetime="", bbox_crs="WGS84"):
        if bbox is None:
            bbox = [-180, -90, 180, 90]
        return self.getCollection(collection_id, bbox, datetime, bbox_crs)

    @staticmethod
    def name():
        return 'Collections'
