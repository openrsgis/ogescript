import json
from . import oge_exception
import six
from . import serializer
import requests
# from .http_util import HTTPUtil
# from pyodide.http import open_url


def getAlgorithms():
    """Get the list of algorithms.

  Returns:
    The dictionary of algorithms.  Each algorithm is a dictionary containing
    the following fields:
        "description" - (string) A text description of the algorithm.
        "returns" - (string) The return type of the algorithm.
        "args" - An array of arguments.  Each argument specifies the following:
            "name" - (string) The name of the argument.
            "description" - (string) A text description of the argument.
            "type" - (string) The type of the argument.
            "optional" - (boolean) Whether the argument is optional or not.
            "default" - A representation of the default value if the argument
                is not specified.
  """
    # url = (
    # "https://lzy-gis.github.io/web4gis15"
    # )
    # url = (
    # "http://125.220.153.26:8093/algorithm"
    # )
    # url = (
    #    "http://oge.whu.edu.cn/api/oge-python/algorithm"
    # )

    # # state_geo = f"{url}/algorithms.json"
    # data = json.loads(open_url(state_geo).read())
    ###########################################################
    fileLocation = "/mnt/algorithms.json"
    with open(fileLocation,"r",encoding='utf-8') as file:
        data = json.load(file)
        return data
    url = (
        "http://oge.whu.edu.cn/api/oge-python/algorithm/algorithms.json"
    )
    # 发送HTTP GET请求获取JSON文件内容
    response = requests.get(url)
    # 检查响应状态码
    if response.status_code == 200:
        # 解析JSON数据
        data = response.json()
        return data
    else:
        print('请求失败，状态码：', response.status_code)
        return None
    #####################################################
    # with open(".././algorithm_data/algorithms.json", 'r', encoding='UTF-8') as f:
    #     data = json.loads(f.read())
    #     # print(data)
    # return data


def getDAGCode(params):
    if isinstance(params['image'], six.string_types):
        raise oge_exception.OGException('Image as JSON string not supported.')
    if 'version' in params:
        raise oge_exception.OGException(
            'Image version specification not supported.')
    return serializer.encode(params['image'], for_cloud_api=True)


def getMapId(params):
    """Get a Map ID for a given asset.

  Args:
    params: An object containing visualization options with the
            following possible values:
      image - The image to render, as an Image or a JSON string.
          The JSON string format is deprecated.
      version - (number) Version number of image (or latest).
      bands - (comma-separated strings) Comma-delimited list of
          band names to be mapped to RGB.
      min - (comma-separated numbers) Value (or one per band)
          to map onto 00.
      max - (comma-separated numbers) Value (or one per band)
          to map onto FF.
      gain - (comma-separated numbers) Gain (or one per band)
          to map onto 00-FF.
      bias - (comma-separated numbers) Offset (or one per band)
          to map onto 00-FF.
      gamma - (comma-separated numbers) Gamma correction
          factor (or one per band).
      palette - (comma-separated strings) A string of comma-separated
          CSS-style color strings (single-band previews only). For example,
          'FF0000,000000'.
      format - (string) The desired map tile image format. If omitted, one is
          chosen automatically. Can be 'jpg' (does not support transparency)
          or 'png' (supports transparency).

  Returns:
    A map ID dictionary containing:
    - "mapid" and optional "token" strings: these identify the map.
    - "tile_fetcher": a TileFetcher which can be used to fetch the tile
      images, or to get a format for the tile URLs.
  """
    if 'image' in params:
        if isinstance(params['image'], six.string_types):
            raise oge_exception.OGException('Image as JSON string not supported.')
        if 'version' in params:
            raise oge_exception.OGException(
                'Image version specification not supported.')
        return serializer.encode(params['image'], for_cloud_api=True)

    elif 'cube' in params:
        if isinstance(params['cube'], six.string_types):
            raise oge_exception.OGException('Cube as JSON string not supported.')
        return serializer.encode(params['cube'], for_cloud_api=True)
    elif 'processResult' in params:
        if isinstance(params['processResult'], six.string_types):
            raise oge_exception.OGException('ProcessResult as JSON string not supported.')
        return serializer.encode(params['processResult'], for_cloud_api=True)
    # request = {
    #     'expression':
    #         serializer.encode(params['image'], for_cloud_api=True),
    #     'fileFormat':
    #         _cloud_api_utils.convert_to_image_file_format(params.get('format')),
    #     'bandIds':
    #         _cloud_api_utils.convert_to_band_list(params.get('bands')),
    # }
    #
    # return {'mapid': map_name, 'token': '',
    #         'tile_fetcher': TileFetcher(url_format, map_name=map_name)}


def computeValue(obj):
    """Sends a request to compute a value.

  Args:
    obj: A ComputedObject whose value is desired.

  Returns:
    The result of evaluating that object on the server.
  """
    body = {'expression': serializer.encode(obj, for_cloud_api=True)}
    print(body)
    # res = HTTPUtil.postRequest(url="http://localhost:8085/oge-dag/getInfo", param=body)
    # print(res)
