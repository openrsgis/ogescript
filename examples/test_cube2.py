# import os
# import sys
# module_path = os.path.abspath(os.path.join('..'))
# if module_path not in sys.path:
#     sys.path.append(module_path)

import oge.mapclient

oge.initialize()

# 根据筛选参数生成Cube， productIds指定数据
params = {"productIds": ["GF_Hainan_Daguangba_NDWI_EO", "Hainan_Daguangba_Village_Vector", "Hainan_Daguangba_VillagePopulation_Tabular"],
          "StartTime": "2016-06-01 00:00:00", "EndTime": "2016-09-01 00:00:00", "geom": [108.90494046724021, 18.753457222586285, 109.18763565740333, 19.0497805438586]}
# image_params1 = {"productName": "LE07_L1TP_ARD_EO", "measurementName": "Near-Infrared",
#                  "geom": (113.054, 29.8, 114.588, 30.774)}
# image1 = oge.Image(image_params1)
# image1.getInfo()
# cube = oge.Cube.load(["GF_Hainan_Daguangba_NDWI_EO", "Hainan_Daguangba_Village_Vector", "Hainan_Daguangba_VillagePopulation_Tabular"], "2016-06-01 00:00:00", "2016-09-01 00:00:00")
cube = oge.Cube(params)
# image2 = image1.add(cube)

# strs = type(cube)
# 对Landsat产品中的每一景影像做NDWI 结果产品名为NDWI
NDWICube = cube.NDWI("Landsat", "NDWI")
# 对NDWI计算changeDetection 结果是ChangeDetection 指定用2018-01-02 和 2018-07-07的两张做比较
ChangeCube = NDWICube.ChangeDetection("NDWI", ["2016-08-15 12:00:00", "2016-08-20 12:00:00"], "ChangeDetection")
# 对ChangeDetection和Vector进行叠置分析 结果是AffectedFeature
AffectedFeatureCube = ChangeCube.OverlayAnalysis("ChangeDetection", "Hainan_Daguangba_Village_Vector", "AffectedFeature")
# 对AffectedFeature和Hainan_VillagePopulation_Tabular进行联合分析 结果是FinalAffectedPoint
FinalAffectedPoint = AffectedFeatureCube.ConjointAnalysis("AffectedFeature", "Hainan_Daguangba_VillagePopulation_Tabular",
                                                          "FinalAffectedPoint")
# 可视化参数 products为可视化的数据列表
vis_params = {"products": ["ChangeDetection", "AffectedFeature"]}
oge.mapclient.addToMap(FinalAffectedPoint, vis_params)


# vis_params = {"products": ["ChangeDetection", "AffectedFeature"]}
# oge.mapclient.addToMap(image2, vis_params)

