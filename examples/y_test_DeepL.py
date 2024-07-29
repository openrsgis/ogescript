import oge
import datetime

# 初始化
oge.initialize()

service = oge.Service.initialize()
# 高分影像获取
BJ2 = service.getCoverage(coverageID="BJ2002F8CVI_00220211229C10_COG")
# 利用深度学习模型进行土地分割
farmlandImage = service.getProcess("Coverage.croplandDetection").execute(BJ2)
# 地图可视化
vis_params = {'min': 0, 'max': 1}
oge.mapclient.centerMap(101.2275, 25.1425, 15)
farmlandImage.styles(vis_params).getMap("croplandDetection")
farmlandImage.styles(vis_params).getMap("croplandDetection2")

