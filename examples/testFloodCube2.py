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
hubeiCube = oge.Cube("Hubei-Cube")
# hubeiCube = service.getCube("Hubei-Cube")
# 按时间维度、空间维度、产品维度切块，得到Landsat产品
hubeiLandsatCube = hubeiCube.filter(datetime=['2020-06-04', '2020-06-05'], geometries=ROI, products=["Landsat8"])
# 反射率由定义的scale factor扩大
hubeiLandsatCube.apply(function="multiply", context={"factor": 0.0000275})
hubeiLandsatCube.apply(function="add", context={"value": -0.2})
# 计算NDWI
hubeiLandsatCube.aggregateDimension(dimension="band", dimensionMembers=[["SR_B3", "SR_B5"]],
                                    function="normalizeDifference",
                                    targetDimensionMembers=["NDWI"]).renameDimension("product", "NDWI")
hubeiLandsatCube.apply(function="gte", context={"threshold": 0})
# 按时间维度、空间维度、产品维度切块，得到Sentinel产品
hubeiSentinelCube = hubeiCube.filter(datetime=['2020-04-17', '2020-04-18'], geometries=ROI, products=["Sentinel"])
# 修改反射率
hubeiSentinelCube.apply(function="divide", context={"value": 10000})
# 计算NDWI
hubeiSentinelCube.aggregateDimension(dimension="band", dimensionMembers=[["B3", "B8"]], function="normalizeDifference",
                                     targetDimensionMembers=["NDWI"]).renameDimension("product", "NDWI")
hubeiSentinelCube.apply(function="gte", context={"threshold": 0})
# 变化检测
hubeiNDWICube = hubeiLandsatCube.merage(hubeiSentinelCube).aggregateDimension(dimension="time",
                                                                              dimensionMembers=[
                                                                                  ["2020-04-17", "2020-06-04"],
                                                                                  ["2020-04-18", "2020-06-05"]],
                                                                              function="subtract",
                                                                              targetDimensionMembers=["t1", "t2"])
POICube = hubeiCube.filter(products=["POI"])
# 叠置分析
affectedPOI = hubeiNDWICube.merge(POICube).aggregateDimension(dimension="product", dimensionMembers=[["NDWI", "POI"]],
                                                              function="overlay",
                                                              targetDimensionMembers=["affectedPOI"])
affectedPOI.styles({"color": "red"}).map()
