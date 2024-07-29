import oge

oge.initialize()
service = oge.Service()

dem = service.getCoverage(coverageID="ASTGTM_N28E056", productID="ASTER_GDEM_DEM30")
n = service.getProcess("Coverage.bandNum").execute(dem)
n.log("n")
# oge.mapclient.centerMap(56.25, 28.40, 11)