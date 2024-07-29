import oge

oge.initialize()
service = oge.Service.initialize()
modisCollection1 = service.getCoverageCollection(productID="MOD13Q1_061", bbox=[73.62, 18.19, 134.7601467382, 53.54],
                                                 datetime=["2022-03-06 00:00:00", "2022-03-06 00:00:00"])
# modisCollection2 = modisCollection1.filter(oge.Filter([oge.Filter.equals("crs", "EPSG:4326"), oge.Filter.equals("measurementName", "NDVI")]))
#modisCollection2 = modisCollection1.filter(oge.Filter.And([oge.Filter.equals("crs", "EPSG:4326"), oge.Filter.equals("measurementName", "NDVI")]))
# modisCollection2 = modisCollection1.filter(oge.Filter.equals("crs", "EPSG:4326"))

modisCollection2 = modisCollection1.filter(oge.Filter([oge.Filter.equals("crs", "EPSG:4326"), oge.Filter.equals("measurementName", ["NDVI","NDBI"])]))







modisCollection2.addStyles().getMap()


