import oge

#初始化
oge.initialize()
service = oge.Service()

#读取数据
landsat8 = service.getCoverage(coverageID="LC08_L1TP_144030_20230831_20230906_02_T1", productID="LC08_L1TP_C02_T1")
DEM = service.getCoverage(coverageID="ASTGTM_N43E084", productID="ASTER_GDEM_DEM30")

# 计算NDVI
ndvi = service.getProcess("Coverage.normalizedDifference").execute(landsat8, ["B5", "B4"])
ndvi_mul = service.getProcess( "Coverage.multiplyNum").execute(ndvi, 100.0)

NaN_value = -9999
# 裁剪出两个栅格数据重叠的部分
ndvi_mul_clip = service.getProcess( "Coverage.rasterUnion").execute(DEM,ndvi_mul)
# dem_clip = service.getProcess( "Coverage.rasterUnion").execute(ndvi_mul_clip,DEM)
#
# #计算坡度和坡向
# slope = service.getProcess( "Coverage.slope").execute(dem_clip, 0.00001171, 3)
#
# #重分类ndvi
# ndvi_reclass = service.getProcess( "Coverage.reclass").execute(ndvi_mul_clip,
#                 [(-50, 0, 1), (0, 10, 2),(10, 20, 3),(20, 30, 4), (30, 40, 5), (40, 50, 6)],NaN_value)

vis_params = {'min': 0, 'max': 360 }
ndvi_mul_clip.styles(vis_params).getMap("ndvi_reclass")
