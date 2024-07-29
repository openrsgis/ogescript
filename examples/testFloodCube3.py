import oge

# 空间筛选几何
ROI = oge.Geometry.Polygon(
    [[[-97.6619468924755, 49.025865329335176],
      [-97.6619468924755, 47.92616126153043],
      [-96.7171226737255, 47.92616126153043],
      [-96.7171226737255, 49.025865329335176]]], None, False)
# 假设湖北省Cube已经提前建立好，里面有Sentinel-2 L2A产品(B3 B8分辨率为10米)和Landsat8 SR产品（SR_B3 SR_B5分辨率30m）以及村庄数据POI（点集要素）
# service = oge.Service()
# 获取湖北省的Cube
hubeiCube = oge.Cube("Hubei-Cube").filter(datetime=['2020-06-04', '2020-06-05'], geometries=ROI)
# 计算Landsat的NDWI
hubeiCube1 = hubeiCube.applyProducts(products=["Landsat_SR_B3", "Landsat_SR_B5"], function="multiply",
                                     param={"factor": 0.0000275})
hubeiCube2 = hubeiCube1.applyProducts(products=["Landsat_SR_B3", "Landsat_SR_B5"], function="add",
                                      param={"value": -0.2})
# 计算Landsat的NDWI
hubeiCube3 = hubeiCube2.apply(function="normalizeDifference",
                              param={"leftValue": "Landsat_SR_B3", "rightValue": "Landsat_SR_B5"}, newProduct="NDWI1")

hubeiCube4 = hubeiCube3.applyProduct(product="NDWI1", function="gte", param={"threshold": 0})
# 修改Sentinel的反射率
hubeiCube5 = hubeiCube4.applyProducts(products=["Sentinel_B3", "Sentinel_B8"], function="divide",
                                      param={"value": 10000})
# 计算Sentinel的NDWI
hubeiCube6 = hubeiCube5.apply(function="normalizeDifference",
                              param={"leftValue": "Sentinel_B3", "rightValue": "Sentinel_B8"}, newProduct="NDWI2")
hubeiCube7 = hubeiCube6.applyProduct(product="NDWI2", function="gte", param={"threshold": 0})
# 沿时间的聚合
hubeiCube8 = hubeiCube7.aggregateDimension(dimension="time", dimensionMembers=[["2020-04-17", "2020-06-04"],
                                                                               ["2020-04-18", "2020-06-05"]],
                                           function="subtract", param={"leftValue": "NDWI1", "rightValue": "NDWI2"},
                                           newDimensionMembers=["t1", "t2"], newProduct="Flood")
# 二值化
hubeiCUbe9 = hubeiCube8.applyProduct(product="Flood", function="gte", param={"threshold": 0})
# 获取POI 这个语义如何决定？ 这里用的latest表示时间上最近的一个POI
POICube = hubeiCube7.aggregateDimension(dimension="time",
                                        dimensionMembers=[["2020-04-17", "2020-06-04"], ["2020-04-18", "2020-06-05"]],
                                        function="latest", param={"product": "POI"},
                                        newDimensionMembers=["t1", "t2"])
# 融合叠置 param可以以字典的形式，也可以以元组的形式("Flood", "POI")
affectedPOI = hubeiCUbe9.fusion(POICube, function="overlay", param={"raster": "Flood", "vector": "POI"},
                                newProduct="AffectedPoint")

affectedPOI.styles({"color": "red"}).map()
