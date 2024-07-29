from . import apifunction
from . import computedobject
from . import data
from . import oge_exception
from . import oge_types
from . import element


class Image(element.Element):
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
                super(Image, self).__init__(
                    apifunction.ApiFunction.lookup('Image.load'),
                    {'id': args, 'version': version})
            else:
                raise oge_exception.OGException(
                    'If version is specified, the arg to Image() must be a string. '
                    'Received: %s' % (args,))
            return

        # 这里增加判断是否是字典类型，由字典类型创建Image
        if isinstance(args, dict):
            keys_to_extract = set(['productName', 'sensorName', 'measurementName', 'StartTime', 'EndTime', 'geom', 'crs', 'method'])
            request = {}
            image_params = {}
            if args:
                for key in args:
                    if key in keys_to_extract:
                        image_params[key] = args[key]
                    else:
                        request[key] = args[key]
            super(Image, self).__init__(
                apifunction.ApiFunction.lookup('Image.load'), image_params)
        elif oge_types.isNumber(args):
            # A constant image.
            super(Image, self).__init__(
                apifunction.ApiFunction.lookup('Image.constant'), {'value': args})
        elif oge_types.isString(args):
            # An ID.
            super(Image, self).__init__(
                apifunction.ApiFunction.lookup('Image.load'), {'id': args})
        elif isinstance(args, (list, tuple)):
            # Make an image out of each element.
            image = Image.combine_([Image(i) for i in args])
            super(Image, self).__init__(image.func, image.args)
        elif isinstance(args, computedobject.ComputedObject):
            if args.name() == 'Array':
                # A constant array image.
                super(Image, self).__init__(
                    apifunction.ApiFunction.lookup('Image.constant'), {'value': args})
            else:
                # A custom object to reinterpret as an Image.
                super(Image, self).__init__(args.func, args.args, args.varName)
        elif args is None:
            super(Image, self).__init__(
                apifunction.ApiFunction.lookup('Image.mask'),
                {'image': Image(0), 'mask': Image(0)})
        else:
            raise oge_exception.OGException(
                'Unrecognized argument type to convert to an Image: %s' % args)

    @classmethod
    def initialize(cls):
        """Imports API functions to this class."""
        if not cls._initialized:
            apifunction.ApiFunction.importApi(cls, 'Image', 'Image')
            cls._initialized = True

    @staticmethod
    def combine_(images, names=None):
        """Combine all the bands from the given images into a single image.

    Args:
      images: The images to be combined.
      names: An array of names for the output bands.

    Returns:
      The combined image.
    """
        if not images:
            raise oge_exception.OGException('Can\'t combine 0 images.')

        # Append all the bands.
        result = Image(images[0])
        for image in images[1:]:
            result = apifunction.ApiFunction.call_('Image.addBands', result, image)

        # Optionally, rename the bands of the result.
        if names:
            result = result.select(['.*'], names)

        return result

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
        response['image'] = self
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
        keys_to_extract = set(['bands', 'gain', 'bias', 'min', 'max',
                               'gamma', 'palette', 'opacity', 'format', 'method'])
        request = {}
        vis_params = {}
        if params:
            for key in params:
                if key in keys_to_extract:
                    vis_params[key] = params[key]
                else:
                    request[key] = params[key]
        image = self
        # GEE中如果可视化是有输入参数的，那么需要调用Image.visualize算子；如果没有，就不需要调用该算子，这里修改不用参数同样调用visualize算子
        if vis_params:
            vis_params['image'] = image
            image = apifunction.ApiFunction.apply_('Image.visualize', vis_params)
        # vis_params['image'] = image
        # image = apifunction.ApiFunction.apply_('Image.visualize', vis_params)
        return image, request

    @staticmethod
    def name():
        return 'Image'
