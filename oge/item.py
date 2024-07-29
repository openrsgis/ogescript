from . import element
from . import apifunction
from . import computedobject
from . import feature
from . import coverage
from . import oge_exception
from . import serializer


class Item(element.Element):
    _initialized = False

    @classmethod
    def initialize(cls):
        if cls._initialized is not True:
            apifunction.ApiFunction.importApi(cls, 'Item', 'Item')
            cls._initialized = True

    def __init__(self, args):
        if isinstance(args, computedobject.ComputedObject):
            super(Item, self).__init__(args.func, args.args, args.varName)
        else:
            raise oge_exception.OGException(
                'Unrecognized argument type to convert to an Image: %s' % args)

    def toFeature(self):
        return feature.Feature(self)

    def toCoverage(self):
        return coverage.Coverage(self)

    @staticmethod
    def name():
        return 'Item'

    def styles(self, args="None"):
        vis_params = {"input": self, "args": args}
        return apifunction.ApiFunction.apply_('Item.addStyles', vis_params)

    def map(self):
        return serializer.encode(self, for_cloud_api=True)["values"]
