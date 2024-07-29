import oge

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

cube1 = oge.Cube()
# 灾后水体，以Landsat8 SR产品作为数据源
l8Col = oge.CoverageCollection("LANDSAT/LC08/C02/T1_L2")\
    .subCollection(datetime=['2020-06-04', '2020-06-05'], geometries=ROI, filter=oge.Filter.lt('CLOUD_COVER', 20))
cube1.add(l8Col, 'Landsat')
cube1.apply(function="multiply", context={"factor": 0.0000275})
cube1.apply(function="add", context={"value": -0.2})
cube1.aggregateDimension(dimension="band", dimensionMembers=[["SR_B3", "SR_B5"]], function="normalizeDifference", targetDimensionMembers=["NDWI"]).renameDimension("product", "NDWI")
cube1.apply(function="gte", context={"threshold": 0})
cube2 = oge.Cube()
s2Col = oge.CoverageCollection("COPERNICUS/S2_SR_HARMONIZED")\
    .subCollection(datetime=['2020-04-17', '2020-04-18'], geometries=ROI, filter=oge.Filter.lt('CLOUD_COVER', 20))
cube2 = oge.Cube()
cube2.add(s2Col, 'Sentinel')
cube2.apply(function="divide", context={"value": 10000})
cube2.aggregateDimension(dimension="band", dimensionMembers=[["B3", "B8"]], function="normalizeDifference", targetDimensionMembers=["NDWI"]).renameDimension("product", "NDWI")
cube2.apply(function="gte", context={"threshold": 0})
cube3 = cube2.merge(cube1)
cube3.aggregateDimension(dimension="time", dimensionMembers=[["2020-04-17", "2020-06-04"], ["2020-04-18", "2020-06-05"]],
                         function="subtract", targetDimensionMembers=["t1", "t2"])
cube3.add(POI, 'POI')
cube3.aggregateDimension(dimension="product", dimensionMembers=[["NDWI", "POI"]],
                         function="overlay", targetDimensionMembers=["affectedPOI"])




