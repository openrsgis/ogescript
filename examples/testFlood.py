import oge


def recalculateReflectanceLandsat(image):
    opticalBands = image.select('SR_B.').multiply(0.0000275).add(-0.2)
    thermalBands = image.select('ST_B.*').multiply(0.00341802).add(149.0)
    return image.addBands(opticalBands, None, True).addBands(thermalBands, None, True)


def calculateNDWILandsat(image):
    return image.addBands(image.normalizedDifference(['SR_B3', 'SR_B5']).rename('NDWI'))


def calculateNDWISentinel(image):
    return image.addBands(image.normalizedDifference(['B3', 'B8']).rename('NDWI'))


def recalculateReflectanceSentinel(image):
    return image.divide(10000)


POI = oge.FeatureCollection(
    [oge.Feature(
        oge.Geometry.Point([-96.7836719974225, 48.840761862783665]),
        {
            "system:index": "0"
        }),
        oge.Feature(
            oge.Geometry.Point([-96.6847950442975, 48.47427993859638]),
            {
                "system:index": "1"
            }),
        oge.Feature(
            oge.Geometry.Point([-97.10776867711, 48.41233280350002]),
            {
                "system:index": "2"
            }),
        oge.Feature(
            oge.Geometry.Point([-97.4318653567975, 48.079448150218276]),
            {
                "system:index": "3"
            }),
        oge.Feature(
            oge.Geometry.Point([-97.1352344974225, 48.75391834534599]),
            {
                "system:index": "4"
            })])
ROI = oge.Geometry.Polygon(
    [[[-97.6619468924755, 49.025865329335176],
      [-97.6619468924755, 47.92616126153043],
      [-96.7171226737255, 47.92616126153043],
      [-96.7171226737255, 49.025865329335176]]], None, False)
# 灾后水体，以Landsat8 SR产品作为数据源
l8Col = oge.CoverageCollection("LANDSAT/LC08/C02/T1_L2").filterDate('2020-06-04', '2020-06-05').filterBounds(ROI) \
    .filter(oge.Filter.lt('CLOUD_COVER', 20)).map(recalculateReflectanceLandsat).map(calculateNDWILandsat)

l8Col_NDWI = l8Col.select('NDWI')

# 镶嵌影像以覆盖研究区域
l8Col_NDWI_mosaic = l8Col_NDWI.mosaic()

# 二值化提取灾后水体
l8Col_water = l8Col_NDWI_mosaic.gte(0)

# 灾中水体，以Sentinel - 2L2A产品作为数据源 为方便数据存储，反射率值由定义的scale factor扩大，此处重新定标反射率的值
s2Col = oge.CoverageCollection('COPERNICUS/S2_SR_HARMONIZED').filterDate('2020-04-17', '2020-04-18') \
    .filterBounds(ROI).filter(oge.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)).map(recalculateReflectanceSentinel).map(
    calculateNDWISentinel)

s2Col_NDWI = s2Col.select('NDWI')
# 镶嵌影像以覆盖研究区域
s2Col_NDWI_mosaic = s2Col_NDWI.mosaic()
# 二值化提取灾中水体
s2Col_water = s2Col_NDWI_mosaic.gte(0)
# 提取洪涝，即灾中水体减去灾后水体
flood = s2Col_water.subtract(l8Col_water)

# 提取受洪涝影响的点 由点提取flood影像的值，以此判断是否受洪涝影响
points = flood.sampleRegions({
    "collection": POI,
    "scale": 30,
    "geometries": True,
})
affectedPoints = points.filter(oge.Filter.eq('NDWI', 1))
affectedPoints.styles({"color": 'red'}).map('Affected Points')
