import oge.mapclient

oge.initialize()

# initialize the OGC API endpoint
service = oge.Service.initialize()
coverageArray = service.getCoverageArray(productID = "GF1_L1_PMS1_EO", datetime = "[2000-01-01 00:00:00,2023-12-31 00:00:00]", bbox = "[114.3, 30, 114.5, 31]")
floatCoverageArray = service.getProcess("CoverageArray.toFloat").execute(coverageArray)
ndviCoverageArray = service.getProcess("CoverageArray.normalizedDifference").execute(floatCoverageArray, ["MSS1_band2", "MSS1_band4"])

vis_params = {"min": -1, "max": 1, "palette": ["#808080", "#949494", "#a9a9a9", "#bdbebd", "#d3d3d3","#e9e9e9"]}
ndviCoverageArray.styles(vis_params).getMap("aspect")
oge.mapclient.centerMap(114.3, 30.5, 8)