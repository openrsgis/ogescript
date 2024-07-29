# import oge
# import oge.mapclient
#
# oge.initialize()
# image_params1 = {"productName": "MOD13Q1_061","crs": "EPSG:4326", "measurementName": "NDVI","geom": [73.6200000000,18.1900000000,134.7601467382,53.5400000000],
#                 "StartTime": "2022-01-01 00:00:00", "EndTime": "2022-12-31 00:00:00", "method": "timeseries"}
# image1 = oge.Image(image_params1)
# image2 = image1.binaryzation(100)
# vis_params = {'min': 0, 'max': 255, 'method':"timeseries"}
# oge.mapclient.addToMap(image2, vis_params, 'test')

import oge

oge.initialize()
# 数据源来自http://example1/
service1 = oge.Service.initialize("http://example1/")
luojiaCollection = service1.getCoverageCollection(productID="LJ01_L2", bbox=[73.62, 18.19, 134.7601467382, 53.54],
                                                  datetime=["2018-09-15 14:39:50", "2018-09-15 14:39:55"])
# mosaic来自http://example2/
service2 = oge.Service.initialize("http://example2/")
image1 = service2.getProcess("CoverageCollection.mosaic").execute(luojiaCollection, "max")

# binaryzation来自http://example3/
service3 = oge.Service.initialize("http://example3/")
image2 = service3.getProcess("Coverage.binaryzation").execute(image1, 220)

# 可视化
vis_params = {'min': 0, 'max': 255}
image2.styles(vis_params).map()
