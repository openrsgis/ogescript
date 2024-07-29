import json
from . import element
from . import computedobject
from . import apifunction
from . import data
from . import serializer
from . import http_util


class ProcessResult(element.Element):
    _initialized = False
    def __init__(self, args=None, version=None):
        self.initialize()
        """Constructs a collection by initializing its ComputedObject."""
        if isinstance(args, computedobject.ComputedObject):
            # A custom object to reinterpret as an Image.
            super(ProcessResult, self).__init__(args.func, args.args, args.varName)
        elif args is None:
            super(ProcessResult, self).__init__(None, None, None)

    @classmethod
    def initialize(cls):
        """ change the execute function input and return """
        if not cls._initialized:
            apifunction.ApiFunction.importApi(cls, 'ProcessResult', 'ProcessResult')
            cls._initialized = True

    def _apply_visualization(self, params):
        request = {}
        vis_params = {}
        process_result = self
        if vis_params:
            vis_params['input'] = process_result
            process_result = apifunction.ApiFunction.apply_('ProcessResult.visualize', vis_params)
        return process_result, request

    def getMapId(self, vis_params=None):
        """Fetch and return a map ID dictionary, suitable for use in a Map overlay.

        Args:
          vis_params: The visualization parameters.  See ee.data.getMapId.

        Returns:
          A map ID dictionary as described in ee.data.getMapId.
        """
        vis_result, request = self._apply_visualization(vis_params)
        request['processResult'] = vis_result
        response = data.getMapId(request)
        response['processResult'] = self
        return response

    @staticmethod
    def name():
        return 'ProcessResult'

    def styles(self, args="None"):
        vis_params = {"input": self, "args": args}
        return apifunction.ApiFunction.apply_('ProcessResult.addStyles', vis_params)

    # def map(self):
    #     dagJson = json.dumps(serializer.encode(self, for_cloud_api=True)["values"])
    #     http_util.HTTPUtil.postDagJson(dagJson)
    #     # return serializer.encode(self, for_cloud_api=True)["values"]
