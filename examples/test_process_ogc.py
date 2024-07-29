import oge

oge.initialize()
# 初始化Service
service = oge.Service.initialize("http//125.220.153.26:8087/geocube/gdc_api_v2/")
image1 = service.getCoverage("LC08_L1TP_ARD_EO", "LC08_L1TP_ARD_EO_20171217025629")
image1.getInfo()