import oge.mapclient

# 初始化
oge.initialize()

service = oge.Service.initialize()


def NDVI(image):
    return service.getProcess("Coverage.normalizedDifference").execute(image, ["B4", "B5"])

# Landsat8数据集获取
landsat8Collection = service.getCoverageCollection(productID="LC08_L1TP_C01_T1",
                                                   bbox=[111.23, 29.31, 116.80, 31.98],
                                                   datetime=["2018-11-26 00:00:00", "2018-12-01 00:00:00"])
ndviCollection = landsat8Collection.map(NDVI)
# 地图可视化
vis_params = {'min': 0, 'max': 1, 'palette': ["blue", "qian blue", "zongSe", "qian green", "green"]}
oge.mapclient.centerMap(113.5, 24.5, 5)
landsat8Collection.styles(vis_params).getMap("ndvi")
# ndviCollection.styles(vis_params).getMap("ndvi")
