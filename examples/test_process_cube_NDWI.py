import oge

oge.initialize()
service = oge.Service.initialize()
cube = service.getCollections(productIDs=['LC08_L1TP_ARD_EO'],
                              datetime=['2000-10-01 00:00:00', '2020-10-01 00:00:00'],
                              bbox=[113.0149404672, 30.0734572226, 113.9181165740, 30.9597805439]
                              ).toCube(bands=['Green', 'Near-Infrared'])
NDWICube = service.getProcess('Cube.NDWI').execute(cube, 'LC08_L1TP_ARD_EO', 'NDWI_Product')
BinaryCube = service.getProcess('Cube.binarization').execute(NDWICube, 'NDWI_Product', 0, 'Binarization_Product')
vis_params = {'products': ['Binarization_Product']}
BinaryCube.styles(vis_params).map()
