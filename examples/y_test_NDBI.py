import oge

# 初始化
oge.initialize()
service = oge.Service()

# 影像数据获取
imageCollection = service.getCoverageCollection(productID="LE07_L1TP_C01_T1", bbox=[113.054, 29.8, 114.588, 30.774],
                                                datetime=["2014-01-01 00:00:00", "2016-12-31 00:00:00"])

imageMosaic = service.getProcess("CoverageCollection.mosaic").execute(imageCollection, "min")

# 影像拼接, 计算NDBI
NDBI = service.getProcess("Coverage.normalizedDifference").execute(imageMosaic, ["Near-Infrared", "SWIR 1"])

# 二值化
result = service.getProcess("Coverage.binarization").execute(NDBI, 0)
# 地图可视化
vis_params = {'min': 0, 'max': 1, 'palette': ["white", "black"]}
oge.mapclient.centerMap(114.2, 30.6, 10)
result.styles(vis_params).getMap("NDBI")
