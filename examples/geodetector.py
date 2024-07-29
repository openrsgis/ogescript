import oge

#初始化
oge.initialize()
service = oge.Service()

#读取数据
landsat8 = service.getCoverage(coverageID="LC08_L1TP_144030_20230831_20230906_02_T1", productID="LC08_L1TP_C02_T1")
landsat8_double = service.getProcess("Coverage.toDouble").execute(landsat8)
DEM = service.getCoverage(coverageID="ASTGTM_N43E084", productID="ASTER_GDEM_DEM30")

# 计算NDVI
ndvi = service.getProcess("Coverage.normalizedDifference").execute(landsat8_double, ["B5", "B4"])
ndvi_mul = service.getProcess( "Coverage.multiplyNum").execute(ndvi, 100.0)

# 裁剪出两个栅格数据重叠的部分
ndvi_mul_clip = service.getProcess( "Coverage.rasterUnion").execute(DEM,ndvi_mul)
dem_clip = service.getProcess( "Coverage.rasterUnion").execute(ndvi_mul_clip,DEM)

#计算坡度和坡向
slope = service.getProcess( "Coverage.slope").execute(dem_clip, 0.00001171,3 )
aspect = service.getProcess( "Coverage.aspect").execute(dem_clip, 1)

#设定规则，对dem、slope、aspect和ndvi进行重分类
NaN_value = -9999
#重分类dem

dem_reclass = service.getProcess( "Coverage.reclass").execute(dem_clip,
            [(500, 1500, 1), (1500, 2500, 2),(2500, 3000, 3), (3000, 3500, 4), (3500, 4500, 5)],NaN_value)
#重分类slope
slope_reclass = service.getProcess( "Coverage.reclass").execute(slope,
            [(0, 5, 1), (5, 15, 2),(15, 25, 3), (25, 35, 4), (35, 45, 5), (45, 90, 6)],NaN_value)
#重分类aspect
aspect_reclass = service.getProcess( "Coverage.reclass").execute(aspect,
    [(0, 60, 1), (60, 120, 2), (120, 180, 3),(180, 240, 4), (240, 300, 5), (300, 360, 6)],NaN_value)
#重分类ndvi
ndvi_reclass = service.getProcess( "Coverage.reclass").execute(ndvi_mul_clip,
                [(-50, 0, 1), (0, 10, 2),(10, 20, 3),(20, 30, 4), (30, 40, 5), (40, 50, 6)],NaN_value)

#定义因变量的正常值范围
ndvi_norExtent = [-100,100]
geo_res_dem = service.getProcess( "Coverage.geoDetector").execute(ndvi_mul_clip,
    "dem",dem_reclass,ndvi_norExtent[0],ndvi_norExtent[1],NaN_value
)
geo_res_slope = service.getProcess( "Coverage.geoDetector").execute(ndvi_mul_clip,
    "slope",slope_reclass,ndvi_norExtent[0],ndvi_norExtent[1],NaN_value
)
geo_res_aspect = service.getProcess( "Coverage.geoDetector").execute(ndvi_mul_clip,
    "aspect",aspect_reclass,ndvi_norExtent[0],ndvi_norExtent[1],NaN_value
)
geo_res_ndvi = service.getProcess( "Coverage.geoDetector").execute(ndvi_mul_clip,
    "ndvi",ndvi_reclass,ndvi_norExtent[0],ndvi_norExtent[1],NaN_value
)
#打印结果
geo_res_dem.log("geo_res_dem")
geo_res_slope.log("geo_res_slope")
geo_res_aspect.log("geo_res_aspect")
geo_res_ndvi.log("geo_res_ndvi")

# oge.mapclient.centerMap(85.22, 43.16, 10)