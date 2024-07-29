import oge

# initialize oge environment
oge.initialize()

# initialize the remote service
remote_service = oge.Service("http://geos.whu.edu.cn:8097/geocube/gdc_api_v2/")
# retrieve the LC08_L2SP data from remote api endpoint
l8cov = remote_service.getCoverage(coverageID="LC08_L2SP_121040_20221014")
# LC08_L2SP NDWI computation
l8covNDWI = remote_service.getProcess("normalizedDifference").execute(l8cov, ['SR_B3', 'SR_B5'])
l8covNDWIBinary = remote_service.getProcess("binarization").execute(l8covNDWI, 0.1)

# initialize the local service
local_service = oge.Service()
s2cov = local_service.getCoverage(coverageID="S2A_MSIL2A_20220506T024551")
# Sentinel-2 NDWI computation
s2covNDWI = local_service.getProcess("Coverage.normalizedDifference").execute(s2cov, ['B3', 'B8'])
s2covNDWIBinary = local_service.getProcess("Coverage.binarization").execute(s2covNDWI, 0)

# dry zone extraction
dryArea = local_service.getProcess("Coverage.subtract").execute(s2covNDWIBinary, l8covNDWIBinary)

# visualization
vis_params = {'min': 0, 'max': 1, 'palette': ["#dcb90f", "#ffffff"]}
oge.mapclient.centerMap(116.3625, 29.0933, 11)
dryArea.styles(vis_params).getMap("drgArea")
