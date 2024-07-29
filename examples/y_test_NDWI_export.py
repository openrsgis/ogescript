import oge.mapclient

# 初始化
oge.initialize()
service = oge.Service()


# Landsat7数据集获取
landsat7 = service.getCoverage(coverageID="LE71230392014351EDC00")
# landsat7Double = service.getProcess("Coverage.toDouble").execute(landsat7)
ndwi = service.getProcess("Coverage.normalizedDifference").execute(landsat7, ["B4", "B5"])
ndict = service.getProcess("Coverage.dictTest").execute(landsat7, {"as": "a", "sa": {"s" : "a"}})
# 地图可视化
vis_params = {'min': -1, 'max': 1, 'palette': [[["#FFA501", "#EEE8AA", "#FFA501", "#1E90FF", "#0000FF"]]]}
oge.mapclient.centerMap(113.87, 30.67, 9)
ndict.styles(vis_params).getMap("s")
# ndwi.styles(vis_params).export({'crs': "EPSG:4326", 'scale': 1000})