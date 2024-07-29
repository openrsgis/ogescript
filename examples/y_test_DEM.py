import oge

# 初始化
oge.initialize()
service = oge.Service.initialize()
# DEM数据获取
dem = service.getCoverage(coverageID="n031e114")
# 山地阴影分析
hillShade = service.getProcess("Coverage.hillShade").execute(dem, 1, 300.0, 40.0)
# 坡度
slope = service.getProcess("Coverage.slope").execute(dem, 1, 300.0, 40.0)
# 坡向
aspect = service.getProcess("Coverage.aspect").execute(dem, 1, 300.0, 40.0)
# 地图可视化
vis_params = {'min': 0, 'max': 255}
oge.mapclient.centerMap(114.2, 30.6, 12)
hillShade.styles(vis_params).getMap('hillShade')
slope.styles(vis_params).getMap('slope')
aspect.styles(vis_params).getMap('aspect')
