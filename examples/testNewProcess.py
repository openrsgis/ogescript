import oge

oge.initialize()
service = oge.Service.initialize("https://10.101.51.3:8099/coverages_api/")
service2 = oge.Service.initialize()
B3 = service.getCoverage("landsat8", "LC08_L1TP_123039_20181102_20181115_01_T1-B3")
B5 = service.getCoverage("landsat8", "LC08_L1TP_123039_20181102_20181115_01_T1-B5")
temp1 = service2.getProcess("Coverage.subtract").execute(B3, B5)
temp2 = service2.getProcess("Coverage.add").execute(B3, B5)
ndwi = service2.getProcess("Coverage.divide").execute(temp1, temp2)
vis_params = {'min': 0, 'max': 255}
ndwi.styles(vis_params).getMap()
