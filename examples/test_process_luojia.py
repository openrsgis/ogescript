import oge

oge.initialize()
service = oge.Service.initialize()
luojiaCollection1 = service.getCoverageCollection(productID="LJ01_L2", bbox=[73.62, 18.19, 134.7601467382, 53.54],
                                                  datetime=["2018-09-15 14:39:50", "2018-09-15 14:39:55"])
luojiaCollection2 = luojiaCollection1.subCollection(filter=oge.Filter.equals("crs", "EPSG:4326"))
luojiaCollection3 = service.getProcess("CoverageCollection.binarization").execute(luojiaCollection2, 1)
vis_params = {'min': 0, 'max': 255}
luojiaCollection3.styles(vis_params).getMap()