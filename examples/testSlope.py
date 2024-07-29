import oge
import oge.mapclient

# dem_params = {"productName": "DEM",
#                  "geom": (113.054, 29.8, 114.588, 30.774)}
# dem = oge.Coverage(dem_params)
# dem2 = dem.Slope(1.0)
# vis_params = {'min': 0, 'max': 255}
# oge.mapclient.addToMap(dem2, vis_params, 'test')


# oge.initialize()
# service = oge.Service.initialize()
# dem = service.getCoverage("DEMProduct", "dem")
# # slopeDem = service.getProcess("Slope").execute(dem, 1.0)
# slopeDem = service.process("slope", dem, 1.0)
# vis_params = {'min': 0, 'max': 255}
# coverage7 = slopeDem.styles(vis_params)
# coverage7.getMap()

# dict = {'s1': 1, 's2': 's', 's3': 'ssss', 's': ['s']}
# print(dict)
# # dictList = [1, 's', 'sssss', 2.0, ['sssss']]
# # print(dictList)
# dictt = (1 , 's', [1, 2])
# print(dictt)

import oge

oge.initialize()
service = oge.Service.initialize()
demCollection1 = service.getCoverageCollection(productID="ASTER_GDEM_DEM30", bbox=[29.1, 114.1, 29.9, 114.9],
                                                    datetime=["2000-01-01 00:00:00", "2000-01-01 00:00:00"])
demCollection2 = demCollection1.subCollection(filter=oge.Filter.equals("crs", "EPSG:4326"))
slopeCollection = service.getProcess("CoverageCollection.slope").execute(demCollection2, 1)
vis_params = {'min': 0, 'max': 255}
slopeCollection.styles(vis_params).getMap()
