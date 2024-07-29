import oge.mapclient

# 初始化
oge.initialize()

service = oge.Service.initialize()


def NDVI(image):
    a = service.getProcess("Coverage.selectBands").execute(image, ["B4"])
    b = service.getProcess("Coverage.selectBands").execute(image, ["B3"])
    c = service.getProcess("Coverage.add").execute(a, b)
    d = service.getProcess("Coverage.subtract").execute(a, b)
    return service.getProcess("Coverage.divide").execute(d, c)


# Landsat8数据集获取
landsat7Collection = service.getCoverageCollection(productID="LE07_L1TP_C01_T1",
                                                   bbox=[111.23, 29.31, 116.80, 31.98],
                                                   datetime=["2013-01-01 00:00:00", "2013-12-31 00:00:00"])
ndviCollection = landsat7Collection.map(NDVI)
# 地图可视化
vis_params = {'min': 0, 'max': 1, 'palette': ["red", "blue", "yellow"]}
oge.mapclient.centerMap(113.5, 24.5, 5)
ndviCollection.styles(vis_params).getMap("ndvi")
