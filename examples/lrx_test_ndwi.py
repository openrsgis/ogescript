import oge.mapclient

# 初始化
oge.initialize()

service = oge.Service.initialize()


def NDVI(image):
    return service.getProcess("Coverage.normalizedDifference").execute(image, ["B4", "B5"])

# Landsat8数据集获取
landsat7Collection = service.getCoverageCollection(productID="LE07_L1TP_C01_T1",
                                                   bbox=[111.23, 29.31, 116.80, 31.98],
                                                   datetime=["2013-01-01 00:00:00", "2013-12-31 00:00:00"])
ndviCollection = landsat7Collection.map(NDVI)
ndviCoverage = service.getProcess("CoverageCollection.sum").execute(ndviCollection)
# 地图可视化
vis_params1 = {'min': 0, 'max': 255}
vis_params2 = {'min': 0, 'max': 1, 'palette': ["red", "blue", "yellow"]}
oge.mapclient.centerMap(113.5, 24.5, 5)
landsat7Collection.styles(vis_params1).getMap("landsat7")
ndviCoverage.styles(vis_params2).getMap("ndwi")
