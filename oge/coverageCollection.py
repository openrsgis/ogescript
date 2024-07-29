import json

from . import apifunction, serializer
from . import computedobject
from . import data
from . import oge_exception
from . import oge_list
from . import oge_types
from . import image
from . import element
from . import coverage
from . import http_util


class CoverageCollection(element.Element):
    """Representation for an Earth Engine ImageCollection."""

    _initialized = False

    def __init__(self, args):
        """ImageCollection constructor.
    Args:
       args: ImageCollections can be constructed from the following arguments:
           1) A string: assumed to be the name of a collection,
           2) An array of images, or anything that can be used to construct an
              image.
           3) A single image.
           5) A computed object - reinterpreted as a collection.
    Raises:
      EEException: if passed something other than the above.
    """
        self.initialize()

        # Wrap single images in an array.
        if isinstance(args, image.Image):
            args = [args]

        if oge_types.isString(args):
            # An ID.
            super(CoverageCollection, self).__init__(
                apifunction.ApiFunction.lookup('ImageCollection.load'), {'id': args})
        elif isinstance(args, dict):
            keys_to_extract = set(['baseUrl', 'productID', 'datetime', 'bbox', 'bboxCrs', 'cloudCoverMin','cloudCoverMax'])
            request = {}
            params = {}
            if args:
                for key in args:
                    if key in keys_to_extract:
                        params[key] = args[key]
                    else:
                        request[key] = args[key]
            super(CoverageCollection, self).__init__(apifunction.ApiFunction.lookup('Service.getCoverageCollection'),
                                                     params)
        elif isinstance(args, (list, tuple)):
            # A list of images.
            super(CoverageCollection, self).__init__(
                apifunction.ApiFunction.lookup('CoverageCollection.fromCoverages'), {
                    'images': [image.Image(i) for i in args]
                })
        elif isinstance(args, oge_list.List):
            # A computed list of images.
            super(CoverageCollection, self).__init__(
                apifunction.ApiFunction.lookup('CoverageCollection.fromCoverages'), {
                    'images': args
                })
        elif isinstance(args, computedobject.ComputedObject):
            # A custom object to reinterpret as an ImageCollection.
            super(CoverageCollection, self).__init__(args.func, args.args, args.varName)
        else:
            raise oge_exception.OGException(
                'Unrecognized argument type to convert to an ImageCollection: %s' %
                args)

    @classmethod
    def initialize(cls):
        """Imports API functions to this class."""
        if not cls._initialized:
            super(CoverageCollection, cls).initialize()
            apifunction.ApiFunction.importApi(
                cls, 'CoverageCollection', 'CoverageCollection')
            apifunction.ApiFunction.importApi(
                cls, 'reduce', 'CoverageCollection')
            cls._initialized = True

    @classmethod
    def reset(cls):
        """Removes imported API functions from this class."""
        apifunction.ApiFunction.clearApi(cls)
        cls._initialized = False

    def getMapId(self, vis_params=None):
        """Fetch and return a Map ID.
    This mosaics the collection to a single image and return a map ID suitable
    for building a Google Maps overlay.
    Args:
      vis_params: The visualization parameters.
    Returns:
      A map ID dictionary as described in ee.data.getMapId.
    """
        mosaic = apifunction.ApiFunction.call_('CoverageCollection.mosaic', self)
        return mosaic.getMapId(vis_params)

    def select(self, selectors, opt_names=None, *args):
        """Select bands from each image in a collection.
    Args:
      selectors: An array of names, regexes or numeric indices specifying
          the bands to select.
      opt_names: An array of strings specifying the new names for the
          selected bands.  If supplied, the length must match the number
          of bands selected.
      *args: Selector elements as varargs.
    Returns:
      The image collection with selected bands.
    """
        return self.map(lambda img: img.select(selectors, opt_names, *args))

    def first(self):
        """Returns the first entry from a given collection.
    Returns:
      The first entry from the collection.
    """
        return image.Image(apifunction.ApiFunction.call_('Collection.first', self))

    @staticmethod
    def name():
        return 'CoverageCollection'

    @staticmethod
    def elementType():
        return coverage.Coverage

    def getVideoThumbURL(self, params=None):
        """Get the URL for an animated video thumbnail of the given collection.
    Note: Videos can only be created when the image visualization
    creates an RGB or RGBA image.  This can be done by mapping a visualization
    onto the collection or specifying three bands in the params.
    Args:
      params: Parameters identical to getMapId, plus, optionally:
      dimensions -
        (a number or pair of numbers in format WIDTHxHEIGHT) Max dimensions of
        the thumbnail to render, in pixels. If only one number is passed, it is
        used as the maximum, and the other dimension is computed by proportional
        scaling.
      crs - a CRS string specifying the projection of the output.
      crs_transform - the affine transform to use for the output pixel grid.
      scale - a scale to determine the output pixel grid; ignored if both crs
        and crs_transform are specified.
      region - (E,S,W,N or GeoJSON) Geospatial region of the result. By default,
        the whole image.
      format - (string) The output format (only 'gif' is currently supported).
      framesPerSecond - Animation speed.
      Visualization parameters - ['bands', 'gain', 'bias', 'min', 'max',
        'gamma', 'palette', 'opacity', 'forceRgbOutput'] see Earth Engine
         API for ee.Image.visualize for more information.
    Returns:
      A URL to download a thumbnail of the specified ImageCollection.
    Raises:
      EEException: If the region parameter is not an array or GeoJSON object.
    """
        return self._getThumbURL(['gif'], params, thumbType='video')

    def getFilmstripThumbURL(self, params=None):
        """Get the URL for a "filmstrip" thumbnail of the given collection.
    Args:
      params: Parameters identical to getMapId, plus, optionally:
      dimensions -
        (a number or pair of numbers in format WIDTHxHEIGHT) Max dimensions of
        the thumbnail to render, in pixels. If only one number is passed, it is
        used as the maximum, and the other dimension is computed by proportional
        scaling.
      crs - a CRS string specifying the projection of the output.
      crs_transform - the affine transform to use for the output pixel grid.
      scale - a scale to determine the output pixel grid; ignored if both crs
        and crs_transform are specified.
      region - (E,S,W,N or GeoJSON) Geospatial region of the result. By default,
        the whole image.
      format - (string) The output format (e.g., "png", "jpg").
      Visualization parameters - ['bands', 'gain', 'bias', 'min', 'max',
        'gamma', 'palette', 'opacity', 'forceRgbOutput'] see Earth Engine
         API for ee.Image.visualize for more information.
    Returns:
      A URL to download a thumbnail of the specified ImageCollection.
    Raises:
      EEException: If the region parameter is not an array or GeoJSON object.
    """
        return self._getThumbURL(['png', 'jpg'], params, thumbType='filmstrip')

    def _getThumbURL(self, valid_formats, params=None, thumbType=None):
        """Get the URL for a thumbnail of this collection.
    Args:
      valid_formats: A list of supported formats, the first of which is used as
        a default if no format is supplied in 'params'.
      params: Parameters identical to getMapId, plus, optionally:
      dimensions -
        (a number or pair of numbers in format WIDTHxHEIGHT) Max dimensions of
        the thumbnail to render, in pixels. If only one number is passed, it is
        used as the maximum, and the other dimension is computed by proportional
        scaling.
      crs - a CRS string specifying the projection of the output.
      crs_transform - the affine transform to use for the output pixel grid.
      scale - a scale to determine the output pixel grid; ignored if both crs
        and crs_transform are specified.
      region - (E,S,W,N or GeoJSON) Geospatial region of the result. By default,
        the whole image.
      format - (string) The output format
      thumbType: must be either 'video' or 'filmstrip'.
    Returns:
      A URL to download a thumbnail of the specified ImageCollection.
    Raises:
      EEException: If the region parameter is not an array or GeoJSON object.
    """

        def map_function(input_image, input_params):
            # pylint: disable=protected-access
            output_image, request = input_image._apply_spatial_transformations(
                input_params)
            output_image, request = output_image._apply_visualization(request)
            # pylint: enable=protected-access
            return output_image, request

        clipped_collection, request = self._apply_preparation_function(
            map_function, params)

        request['format'] = params.get('format', valid_formats[0])
        if request['format'] not in valid_formats:
            raise oge_exception.OGException(
                'Invalid format specified for thumbnail. ' + str(params['format']))

        if params and 'framesPerSecond' in params:
            request['framesPerSecond'] = params.get('framesPerSecond')
        request['image'] = clipped_collection
        if params and params.get('dimensions') is not None:
            request['dimensions'] = params.get('dimensions')
        if thumbType not in ['video', 'filmstrip']:
            raise oge_exception.OGException(
                'Invalid thumbType provided to _getThumbURL only \'video\' or '
                '\'filmstrip\' is supported.')

        return data.makeThumbUrl(data.getThumbId(request, thumbType=thumbType))

    def _apply_preparation_function(self, preparation_function, params):
        """Applies a preparation function to an ImageCollection.
    Args:
      preparation_function: The preparation function. Takes an image and a
        parameter dict; returns the modified image and a subset of the
        parameter dict, with the parameters it used removed.
      params: The parameters to the preparation function.
    Returns:
      A tuple containing:
      - an ImageCollection that has had many of the parameters applied
        to it
      - any remaining parameters.
    """
        # The preparation function operates only on a single image and returns a
        # modified parameter set; we need to apply across all the images in this
        # collection via self.map, and also return a modified parameter set, which
        # we can't easily get out of self.map. So we invoke it in two ways: once on
        # a dummy Image to get a modified parameter set, and once via self.map.
        _, remaining_params = preparation_function(self.first(), params)

        if remaining_params == params:
            # Nothing in params affects us; omit the map.
            return self, params

        # Copy params defensively in case it's modified after we return but before
        # the map operation is serialised.
        params = params.copy()

        def apply_params(img):
            prepared_img, _ = preparation_function(img, params)
            return prepared_img

        return self.map(apply_params), remaining_params

    def prepare_for_export(self, params):
        """Applies all relevant export parameters to an ImageCollection.
    Args:
      params: The export request parameters.
    Returns:
      A tuple containing:
      - an ImageCollection that has had many of the request parameters applied
        to it
      - any remaining parameters.
    """
        # If the Cloud API is enabled, we can do cleaner handling of the parameters.
        # If it isn't enabled, we have to be bug-for-bug compatible with current
        # behaviour, so we do nothing.
        return self._apply_preparation_function(image.Image.prepare_for_export,
                                                params)

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
            vis_params['coverageCollection'] = self
            return apifunction.ApiFunction.apply_('CoverageCollection.addStyles', vis_params)

    # def getMap(self):
    #     dagJson = json.dumps(serializer.encode(self, for_cloud_api=True)["values"])
    #     http_util.HTTPUtil.postDagJson(dagJson)
    #     # print(DAGJson)
    #     # return serializer.encode(self, for_cloud_api=True)["values"]

    def map(self, algorithm, opt_dropNulls=None):
        """Maps an algorithm over a collection.

    Args:
      algorithm: The operation to map over the images or features of the
          collection, a Python function that receives an image or features and
          returns one. The function is called only once and the result is
          captured as a description, so it cannot perform imperative operations
          or rely on external state.
      opt_dropNulls: If true, the mapped algorithm is allowed to return nulls,
          and the elements for which it returns nulls will be dropped.

    Returns:
      The mapped collection.

    Raises:
      lge_exception.OGException: if algorithm is not a function.
    """
        element_type = self.elementType()
        with_cast = lambda e: algorithm(element_type(e))
        return self._cast(apifunction.ApiFunction.call_(
            'Collection.map', self, with_cast, opt_dropNulls))
