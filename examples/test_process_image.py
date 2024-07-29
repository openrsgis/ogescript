import oge.mapclient

oge.initialize()
service = oge.Service.initialize()
coverage1 = service.getCoverage("LE07_L1TP_ARD_EO", "Near-Infrared")
coverage2 = service.getCoverage("LE07_L1TP_ARD_EO", "Red")

coverage3 = service.getProcess("Coverage.add").execute(coverage1, coverage2)
coverage4 = service.getProcess("Coverage.subtract").execute(coverage1, coverage2)
coverage5 = service.getProcess("Coverage.divide").execute(coverage3, coverage4)
coverage6 = service.getProcess("Coverage.binarization").execute(coverage5, 0)
vis_params = {'min': 0, 'max': 255}
coverage7 = coverage6.styles(vis_params).getMap()

