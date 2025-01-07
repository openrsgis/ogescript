from oge import ApiFunction

from . import collections
from . import collection
from . import element
from . import coverageCollection
from . import coverage
from . import featurecollection
from . import feature
from . import apifunction
from . import process
from . import processes
from . import table
from . import cube
from . import sheet
from . import coverageArray
from . import mlmodel

class Service(element.Element):
    # 类变量
    # _url = "http://localhost"

    def __init__(self, url="http://localhost"):
        # self.initialize(url=self.url)
        self._url = url
        super(Service, self).__init__(None, None, None)

    # @staticmethod
    # def process(process_id):
    #     api_function = ApiFunction.lookup(process_id)
    #     return process.Process(api_function)

    @staticmethod
    def collections(datetime="", bbox=None, bbox_crs="WGS84"):
        if bbox is None:
            bbox = [-180, -90, 180, 90]
        params = {
            'datetime': datetime,
            'bbox': bbox,
            'bbox_crs': bbox_crs
        }
        return collections.Collections(params)

    """
    查询符合条件的数据集
    """

    def getCollections(self, productIDs=None, datetime=None, bbox=None, bbox_crs=None):
        params = {
            'baseUrl': self._url,
            'datetime': datetime,
            'bbox': bbox,
            'bboxCrs': bbox_crs,
            'productIDs': productIDs
        }
        return collections.Collections(params)

    """
    查询指定Id的数据集
    """

    def getCollection(self, collectionId):
        params = {
            'baseUrl': self._url,
            'collectionId': collectionId,
        }
        return collection.Collection(params)

    """
    查询指定Id的要素数据集
    """

    def getFeatureCollection(self, productID, datetime="null", bbox="null", bbox_crs="WGS84", filters="null"):
        param = {
            'baseUrl': self._url,
            'productID': productID,
            'datetime': datetime,
            'bbox': bbox,
            'bboxCrs': bbox_crs,
            'filter': filters
        }
        return featurecollection.FeatureCollection(param)

    """
    查询指定Id的要素
    """

    def getFeature(self, featureId, productID=None,dateTime=None):
        param = {
            'baseUrl': self._url,
            'productID': productID,
            'featureId': featureId,
            'dateTime': dateTime
        }
        return feature.Feature(None, None, param)

    """
    查询指定Id的覆盖数据集
    """

    def getCoverageCollection(self, productID, datetime=None, bbox=None, cloudCoverMin = None, cloudCoverMax = None,bbox_crs=None):
        param = {
            'baseUrl': self._url,
            'productID': productID,
            'datetime': datetime,
            'bbox': bbox,
            'bboxCrs': bbox_crs,
            'cloudCoverMin' : cloudCoverMin,
            'cloudCoverMax' : cloudCoverMax,
        }
        return coverageCollection.CoverageCollection(param)

    """
    查询指定Id的覆盖数据
    """

    def getCoverage(self, coverageID, productID=None, subset=None, properties=None):
        param = {
            'baseUrl': self._url,
            'productID': productID,
            'coverageID': coverageID,
            'subset': subset,
            "properties": properties
        }
        return coverage.Coverage(param)

    def getSheet(self, sheetID):
        param = {
            'baseUrl': self._url,
            'sheetID': sheetID
        }
        return sheet.Sheet(param)


    def getCube(self, cubeId, products, bands, time, extent, tms, resolution):
        param = {
            'baseUrl': self._url,
            'cubeId': cubeId,
            'products': products,
            'bands': bands,
            'time': time,
            'extent': extent,
            'tms': tms,
            'resolution': resolution
        }
        return cube.Cube(param)

    """
    查询处理列表
    """

    def getProcesses(self):
        return processes.Processes(self._url)

    """
    查询特定id的处理
    """

    def getProcess(self, process_id):
        param = {
            "baseUrl": self._url,
            "processId": process_id
        }
        return process.Process(param)

    """
    直接执行特定的处理
    """

    def process(self, process_id, *args, **kwargs):
        target_process = self.getProcess(process_id)
        return target_process.execute(*args, **kwargs)

    """
    查询指定Id的表格数据
    """

    def getTable(self, productID):
        param = {
            'baseUrl': self._url,
            'productID': productID,
        }
        return table.Table(param)

    """
    查询指定Id的机器学习模型
    """

    def getModel(self, modelID):
        param = {
            'baseUrl': self._url,
            'modelID': modelID,
        }
        return mlmodel.MLmodel(param)

    """
    查询指定Id的覆盖数据集
    """
    def getCoverageArray(self, productID, datetime=None, bbox=None, cloudCoverMin=None, cloudCoverMax=None,
                         bbox_crs=None):
        param = {
            'baseUrl': self._url,
            'productID': productID,
            'datetime': datetime,
            'bbox': bbox,
            'bboxCrs': bbox_crs,
            'cloudCoverMin': cloudCoverMin,
            'cloudCoverMax': cloudCoverMax,
        }
        return coverageArray.CoverageArray(param)

    @classmethod
    def initialize(cls, url="http://localhost"):
        """Imports API functions to this class."""
        if not cls._initialized:
            apifunction.ApiFunction.importApi(cls, 'Service', 'Service')
            cls._initialized = True
        return Service(url)

    def getUrl(self):
        return self._url

    @staticmethod
    def name():
        return 'Service'
