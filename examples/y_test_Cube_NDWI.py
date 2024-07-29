import oge

# 初始化
oge.initialize()
service = oge.Service.initialize()
# Cube创建
cube = service.getCollections(productIDs=['LC08_L1TP_ARD_EO'],
                              datetime=['2000-10-01 00:00:00', '2020-10-01 00:00:00'],
                              bbox=[113.0149404672, 30.0734572226, 113.9181165740, 30.9597805439]
                              ).toCube(bands=['Green', 'Near-Infrared'])
NDWICube = service.getProcess('Cube.NDWI').execute(cube, 'LC08_L1TP_ARD_EO', 'NDWI_Product')
# 二值化
BinaryCube = service.getProcess('Cube.binarization').execute(NDWICube, 'NDWI_Product', 0, 'Binarization_Product')
# 地图可视化
vis_params = {'products': ['Binarization_Product'], 'palette': ["yellow", "blue"], "min": 0, "max": 1}
BinaryCube.styles(vis_params).getMap("NDWICube")
oge.mapclient.centerMap(113.5, 30.5, 7)
