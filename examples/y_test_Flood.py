import oge

# 初始化
oge.initialize()
service = oge.Service.initialize()

#
# def NDWI(image, bands):
#     return service.getProcess("Coverage.normalizedDifference").execute(image, bands)


# 影像数据获取
l8col = service.getCoverageCollection(productID="LE08_L1TP_C01_T1",
                                      datetime=["2020-06-04", "2020-06-05"])
# l8colNDWI = l8col.map(NDWI(['SR_B3', 'SR_B5']))
l8colNDWI = l8col.map(lambda image: service.getProcess("Coverage.normalizedDifference").execute(image, ['SR_B3', 'SR_B5']))
l8colNDWIMosaic = service.getProcess("CoverageCollection.mosaic").execute(l8colNDWI, "min")
l8colNDWIMosaicBinary = service.getProcess("Coverage.binarization").execute(l8colNDWIMosaic, 0.1)

s2col = service.getCoverageCollection(productID="S2_SR_HARMONIZED",
                                      datetime=["2020-04-17", "2020-04-18"])
# s2colNDWI = s2col.map(NDWI(bands=['B3', 'B8']))
s2colNDWI = s2col.map(lambda image: service.getProcess("Coverage.normalizedDifference").execute(image, ['B3', 'B8']))
s2colNDWIMosaic = service.getProcess("CoverageCollection.mosaic").execute(s2colNDWI, "min")
s2colNDWIMosaicBinary = service.getProcess("Coverage.binarization").execute(s2colNDWIMosaic, 0)

flood = service.getProcess("Coverage.subtract").execute(s2colNDWIMosaicBinary, l8colNDWIMosaicBinary)
# 地图可视化
vis_params = {'min': 0, 'max': 1, 'palette': ["yellow", "blue"]}
oge.mapclient.centerMap(114.2, 30.6, 10)
flood.styles(vis_params).getMap("flood")
