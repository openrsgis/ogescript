#!/usr/bin/env python
"""Representation of an Earth Engine FeatureCollection."""

# Using lowercase function naming to match the JavaScript names.
# pylint: disable=g-bad-name
# pylint: disable=g-long-lambda
import json

from . import apifunction, serializer
from . import element
from . import computedobject
from . import data
from . import deprecation
from . import oge_exception
from . import oge_list
from . import oge_types
from . import feature
from . import geometry
from . import http_util


class FeatureCollection(element.Element):
    """A representation of a FeatureCollection."""

    _initialized = False

    def __init__(self, args, opt_column=None):
        """Constructs a collection features.

    Args:
      args: constructor argument.  One of:
          1) A string - assumed to be the name of a collection.
          2) A geometry.
          3) A feature.
          4) An array of features.
          5) A GeoJSON FeatureCollection.
          6) A computed object - reinterpreted as a collection.
      opt_column: The name of the geometry column to use. Only useful with the
          string constructor.

    Raises:
      OGException: if passed something other than the above.
    """
        self.initialize()

        # Wrap geometries with features.
        if isinstance(args, geometry.Geometry):
            args = feature.Feature(args)

        # Wrap single features in an array.
        if isinstance(args, feature.Feature):
            args = [args]

        if oge_types.isString(args):
            # An ID.
            actual_args = {'tableId': args}
            if opt_column:
                actual_args['geometryColumn'] = opt_column
            super(FeatureCollection, self).__init__(
                apifunction.ApiFunction.lookup('Collection.loadTable'), actual_args)
        elif isinstance(args, (list, tuple)):
            # A list of features.
            super(FeatureCollection, self).__init__(
                apifunction.ApiFunction.lookup('Collection'), {
                    'features': [feature.Feature(i) for i in args]
                })
        elif isinstance(args, oge_list.List):
            # A computed list of features.
            super(FeatureCollection, self).__init__(
                apifunction.ApiFunction.lookup('Collection'), {
                    'features': args
                })
        elif isinstance(args, dict) and args.get('type') == 'FeatureCollection':
            # A GeoJSON FeatureCollection
            super(FeatureCollection, self).__init__(
                apifunction.ApiFunction.lookup('Collection'),
                {'features': [feature.Feature(i) for i in args.get('features', [])]})
        elif isinstance(args, dict) and args.__contains__("baseUrl"):
            # Service provide the param
            keys_to_extract = set(['baseUrl', "productID", 'datetime', 'bbox', 'bboxCrs', "filter"])
            request = {}
            params = {}
            if args:
                for key in args:
                    if key in keys_to_extract:
                        params[key] = args[key]
                    else:
                        request[key] = args[key]
            super(FeatureCollection, self).__init__(
                apifunction.ApiFunction.lookup('Service.getFeatureCollection'), params)
        elif isinstance(args, computedobject.ComputedObject):
            # A custom object to reinterpret as a FeatureCollection.
            super(FeatureCollection, self).__init__(
                args.func, args.args, args.varName)
        else:
            raise oge_exception.OGException(
                'Unrecognized argument type to convert to a FeatureCollection: %s' %
                args)

    @classmethod
    def initialize(cls):
        """Imports API functions to this class."""
        if not cls._initialized:
            super(FeatureCollection, cls).initialize()
            apifunction.ApiFunction.importApi(
                cls, 'FeatureCollection', 'FeatureCollection')
            cls._initialized = True

    @classmethod
    def reset(cls):
        """Removes imported API functions from this class."""
        apifunction.ApiFunction.clearApi(cls)
        cls._initialized = False

    def getMapId(self, vis_params=None):
        """Fetch and return a map id and token, suitable for use in a Map overlay.

    Args:
      vis_params: The visualization parameters. Currently only one parameter,
          'color', containing a hex RGB color string is allowed.

    Returns:
      A map ID dictionary as described in ee.data.getMapId, including an
      additional 'image' field containing Collection.draw image wrapping a
      FeatureCollection containing this feature.
    """
        painted = apifunction.ApiFunction.apply_('Collection.draw', {
            'collection': self,
            'color': (vis_params or {}).get('color', '000000')
        })
        return painted.getMapId({})

    def getDownloadURL(self, filetype=None, selectors=None, filename=None):
        """Gets a download URL.

    When the URL is accessed, the FeatureCollection is downloaded in one of
    several formats.

    Args:
      filetype: The format of download, one of: "csv", "json", "geojson", "kml",
          "kmz" ("json" outputs GeoJSON). If unspecified, defaults to "csv".
      selectors: Feature property names used to select the attributes to be
          downloaded. If unspecified, all properties are included.
      filename: Name of the file to be downloaded; extension is appended by
          default. If unspecified, defaults to "table".

    Returns:
      A URL to download this FeatureCollection.
    """
        request = {}
        request['table'] = self
        if filetype is not None:
            request['format'] = filetype.upper()
        if filename is not None:
            request['filename'] = filename
        if selectors is not None:
            if isinstance(selectors, (list, tuple)):
                selectors = ','.join(selectors)
            request['selectors'] = selectors
        return data.makeTableDownloadUrl(data.getTableDownloadId(request))

    # Deprecated spelling to match the JS library.
    getDownloadUrl = deprecation.Deprecated('Use getDownloadURL().')(
        getDownloadURL)

    def select(self, propertySelectors, newProperties=None,
               retainGeometry=True, *args):
        """Select properties from each feature in a collection.

    Args:
      propertySelectors: An array of names or regexes specifying the properties
          to select.
      newProperties: An array of strings specifying the new names for the
          selected properties.  If supplied, the length must match the number
          of properties selected.
      retainGeometry: A boolean.  When false, the result will have no geometry.
      *args: Selector elements as varargs.

    Returns:
      The feature collection with selected properties.
    """
        if len(args) or oge_types.isString(propertySelectors):
            args = list(args)
            if not isinstance(retainGeometry, bool):
                args.insert(0, retainGeometry)
            if newProperties is not None:
                args.insert(0, newProperties)
            args.insert(0, propertySelectors)
            return self.map(lambda feat: feat.select(args, None, True))
        else:
            return self.map(
                lambda feat: feat.select(
                    propertySelectors, newProperties, retainGeometry))

    @staticmethod
    def name():
        return 'FeatureCollection'

    @staticmethod
    def elementType():
        return feature.Feature

    def styles(self, color="None"):
        vis_params = {}
        featureCollection = self
        vis_params['input'] = featureCollection
        vis_params['color'] = color
        return apifunction.ApiFunction.apply_('FeatureCollection.addStyles', vis_params)

    # def getMap(self):
    #     # DAGJson = serializer.encode(self, for_cloud_api=True)["values"]
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
