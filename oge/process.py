import re
from . import apifunction
from . import element
from . import computedobject


class Process(element.Element):
    _initialized = False
    _process_id = ""
    _process_function_sig = {
        'description': 'Execute the process by the restful api of OGC',
        'returns': 'ProcessResult',
        'args': []
    }

    def __init__(self, args=None):
        self.initialize()
        if isinstance(args, dict):
            self._base_url = args["baseUrl"]
            self._process_id = args["processId"]
            super(Process, self).__init__(apifunction.ApiFunction.lookup("Service.getProcess"),
                                          args)
        elif isinstance(args, computedobject.ComputedObject):
            # A custom object to reinterpret as an Image.
            self._base_url = args.args["processes"].get_base_url()
            self._process_id = args.args["processId"].getValue()
            super(Process, self).__init__(args.func, args.args, args.varName)
        if self._base_url == "http://localhost":
            self._local_api_function = apifunction.ApiFunction.lookup(self._process_id)

    @classmethod
    def initialize(cls):
        """ change the execute function input and return """
        if not cls._initialized:
            apifunction.ApiFunction.importApi(cls, 'Process', 'Process')
            cls._initialized = True

    @staticmethod
    def extract_type(value):
        s = str(type(value))
        value_type = str(type(value)).replace("'", "").replace("<class ", "").replace(">", "")
        # 分割 首字母大写
        value_type = value_type.split(".")[-1].capitalize()
        return value_type

    def execute(self, *args, **kwargs):
        if self._base_url != "http://localhost":
            args_list = []
            for index in range(len(args)):
                arg = {
                    'name': 'param' + str(index),
                    'type': self.extract_type(args[index]),
                    'description': 'wps param' + str(index)
                }
                args_list.append(arg)
            for key, value in kwargs.items():
                arg = {
                    'name': key,
                    'type': self.extract_type(value),
                    'description': 'wps param' + key
                }
                args_list.append(arg)
            args_list.append({
                'name': 'url',
                'type': 'String',
                'description': self._base_url + '/process/' + self._process_id
            })
            self._process_function_sig['args'] = args_list
            process_function = apifunction.ApiFunction(self._process_id, self._process_function_sig)
            return process_function.call(url=self._base_url + '/processes/' + self._process_id, *args, **kwargs)
        else:
            return self._local_api_function.call(*args, **kwargs)

    @staticmethod
    def name():
        return 'Process'
