#!/usr/bin/env python
"""An object representing EE Features."""

# Using lowercase function naming to match the JavaScript names.
# pylint: disable=g-bad-name
import json

from . import apifunction, serializer
from . import computedobject
from . import oge_exception
from . import element
from . import geometry
from . import http_util


class Feature(element.Element):
    """An object representing EE Features."""

    _initialized = False

    def __init__(self, geom, opt_properties=None, server_param=None):
        """Creates a feature a geometry or computed object.

    Features can be constructed from one of the following arguments plus an
    optional dictionary of properties:
      1) An ee.Geometry.
      2) A GeoJSON Geometry.
      3) A GeoJSON Feature.
      4) A computed object - reinterpreted as a geometry if properties
         are specified, and as a feature if they aren't.

    Args:
      geom: A geometry or feature.
      opt_properties: A dictionary of metadata properties. If the first
          parameter is a Feature (instead of a geometry), this is unused.

    Raises:
      OGException: if the given geometry isn't valid.
    """
        if isinstance(geom, Feature):
            if opt_properties is not None:
                raise oge_exception.OGException(
                    'Can\'t create Feature out of a Feature and properties.')
            # A pre-constructed Feature. Copy.
            super(Feature, self).__init__(geom.func, geom.args)
            return

        self.initialize()

        feature_constructor = apifunction.ApiFunction.lookup('Feature')
        if (geom is None or isinstance(geom, geometry.Geometry)) and server_param is None:
            # A geometry object.
            super(Feature, self).__init__(feature_constructor, {
                'geometry': geom,
                'metadata': opt_properties or None
            })
        elif geom is None and server_param is not None:
            keys_to_extract = set(['baseUrl', 'productID', 'featureId','dateTime'])
            request = {}
            feature_params = {}
            if server_param:
                for key in server_param:
                    if key in keys_to_extract:
                        feature_params[key] = server_param[key]
                    else:
                        request[key] = server_param[key]
            super(Feature, self).__init__(apifunction.ApiFunction.lookup('Service.getFeature'), feature_params)
        elif isinstance(geom, computedobject.ComputedObject):
            # A custom object to reinterpret as a Feature.
            super(Feature, self).__init__(geom.func, geom.args, geom.varName)
        elif isinstance(geom, dict) and geom.get('type') == 'Feature':
            properties = geom.get('properties', {})
            if 'id' in geom:
                if 'system:index' in properties:
                    raise oge_exception.OGException(
                        'Can\'t specify both "id" and "system:index".')
                properties = properties.copy()
                properties['system:index'] = geom['id']
            # Try to convert a GeoJSON Feature.
            super(Feature, self).__init__(feature_constructor, {
                'geometry': geometry.Geometry(geom.get('geometry', None)),
                'metadata': properties
            })
        else:
            # Try to convert the geometry arg to a Geometry, in the hopes of it
            # turning out to be GeoJSON.
            super(Feature, self).__init__(feature_constructor, {
                'geometry': geometry.Geometry(geom),
                'metadata': opt_properties or None
            })

    @classmethod
    def initialize(cls):
        """Imports API functions to this class."""
        if not cls._initialized:
            apifunction.ApiFunction.importApi(cls, 'Feature', 'Feature')
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
        # Create a collection containing this one feature and render it.
        collection = apifunction.ApiFunction.call_('Collection', [self])
        return collection.getMapId(vis_params)

    @staticmethod
    def name():
        return 'Feature'

    def styles(self, color=[],attribute=""):
        vis_params = {}
        feature = self
        vis_params['input'] = feature
        vis_params['color'] = color
        vis_params['attribute'] = attribute
        return apifunction.ApiFunction.apply_('Feature.addStyles', vis_params)

    # def getMap(self):
    #     # DAGJson = serializer.encode(self, for_cloud_api=True)["values"]
    #     dagJson = json.dumps(serializer.encode(self, for_cloud_api=True)["values"])
    #     http_util.HTTPUtil.postDagJson(dagJson)
    #     # print(DAGJson)
    #     # return serializer.encode(self, for_cloud_api=True)["values"]
