import requests
import oge.mapclient
# import json
# from pyodide.http import pyfetch
# import asyncio


class HTTPUtil:

    layer_index = 0

    @staticmethod
    def postRequest(url, param):
        res = requests.post(url=url, data=param)
        return res.text

    @staticmethod
    def getRequest(url, param):
        res = requests.get(url=url, data=param)
        return res.text

    @staticmethod
    def postDagJson(dagJson, layer_name=None):
        params = {"dag": dagJson}
        # space_params = oge.mapclient.getSpaceParams()
        # if space_params is not None:
        #     params["spaceParams"] = space_params
        if layer_name is not None:
            params["layerName"] = layer_name
        else:
            params["layerName"] = "layer" + str(HTTPUtil.layer_index)
            HTTPUtil.layer_index = HTTPUtil.layer_index + 1
            if HTTPUtil.layer_index > 100:
                HTTPUtil.layer_index = 0
        # print(params)
        print("dag=<<" + str(params) + ">>")
        # res = HTTPUtil.postRequest("http://localhost:8085/oge-dag/saveDagJson", json.dumps(params))

        # async def get_data(dag):
        #     # response = await pyfetch('http://125.220.153.26:8085/oge-dag/saveDagJson', method="POST", body=dag)
        #     response = await pyfetch('http://oge.whu.edu.cn/api/oge-dag/saveDagJson', method="POST", body=json.dumps(params))
        #     res = await response.string()
        #     print(res)
        # task = [get_data(dagJson)]
        # loops = asyncio.get_event_loop()
        # loops.run_until_complete(asyncio.wait(task))

    @staticmethod
    def batchDagJson(dagJson, export_params):
        params = {"dag": dagJson, "isBatch": 1, "exportCoverage": export_params}
        print("dag=<<" + str(params) + ">>")
