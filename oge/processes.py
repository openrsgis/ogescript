from . import process
from . import element
from . import apifunction


class Processes(element.Element):
    _initialized = False

    def __init__(self, base_url):
        self.initialize()
        self._base_url = base_url
        super(Processes, self).__init__(
            apifunction.ApiFunction.lookup('Service.getProcesses'), {"baseUrl": base_url})

    @classmethod
    def initialize(cls):
        """ change the execute function input and return """
        if not cls._initialized:
            apifunction.ApiFunction.importApi(cls, 'Processes', 'Processes')
            cls._initialized = True

    def get_base_url(self):
        return self._base_url

    @staticmethod
    def name():
        return 'Processes'
