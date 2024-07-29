import oge.mapclient

oge.initialize()

cube_params_1 = {"productName": "Landsat", "sensorName": "LOC08", "geom": [123, 23, 46, 89], "type": "Raster"}
cube_params_2 = {"productName": "Hainan_Village_Vector", "type": "Feature"}
cube_params_3 = {"productName": "Hainan_VillagePopulation_Tabular", "type": "Tabular"}
# 这里声明Cube对象 对Image Feature Tabular 统一使用lge.Cube() 在声明参数中利用“type“ 进行类型区分
rasterCube = oge.Cube(cube_params_1)
featureCube = oge.Cube(cube_params_2)
tabularCube = oge.Cube(cube_params_3)
fusionCube = rasterCube.fusion(featureCube, "overlay", {"value": 1, "value2": 2}, "point")
fusionCube2 = rasterCube.fusion(featureCube, "overlay", (1, 2, "test"), "point")
fusionCube.getMap()
fusionCube2.getMap()
# NDWICube = rasterCube.NDWI()
# ChangeCube = NDWICube.ChangeDetection()
# AffectedFeatureCube = ChangeCube.OverlayAnalysis(featureCube)
# FinalAffectedPoint = AffectedFeatureCube.ConjointAnalysis(tabularCube)
#
# oge.mapclient.addToMap(FinalAffectedPoint)


