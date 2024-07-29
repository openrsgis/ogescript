import oge

oge.initialize()
# initialize the OGC API endpoint
service = oge.Service("https://oge.whu.edu.com/ogcapi/coverages_api/")
temperature = service.getCoverageCollection("ERA5_2mTemperature_China_Monthly", datetime=["2018-01-01", "2018-12-31"])
precipitation = service.getCoverageCollection("ERA5_TotalPrecipitation_China_Monthly", datetime=["2018-01-01", "2018-12-31"])
# initialize the local service
localService = oge.Service()
spei_result = localService.getProcess("SPEI", temperature, precipitation, 1)
# result render
vis_params = {'min': -2.0, 'max': -0.5, 'palette': ["#8B572A", "#D26E16", "#F8E71C", "#7ED321", "#4A90E2"]}
spei_result.styles(vis_params).getMap("SPEI")