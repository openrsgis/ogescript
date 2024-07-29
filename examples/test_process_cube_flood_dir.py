import oge

oge.initialize()
service = oge.Service.initialize()
cube = service.getCollections(productIDs=["GF_Hainan_Daguangba_NDWI_EO", "Hainan_Daguangba_Village_Vector",
                                          "Hainan_Daguangba_VillagePopulation_Tabular"],
                              datetime=["2016-06-01 00:00:00", "2016-09-01 00:00:00"],
                              bbox=[108.90494046724021, 18.753457222586285, 109.18763565740333, 19.0497805438586]
                              ).toCube()
ChangeCube = service.getProcess("Cube.subtract").execute(
    cube, "GF_Hainan_Daguangba_NDWI_EO", ["2016-08-15 12:00:00", "2016-08-20 12:00:00"], "Change_Product")
AffectedFeatureCube = service.getProcess("Cube.overlayAnalysis").execute(
    ChangeCube, "Change_Product", "Hainan_Daguangba_Village_Vector", "AffectedFeature_Product")
FinalAffectedPoint = service.getProcess("Cube.overlayAnalysis").execute(
    AffectedFeatureCube, "Hainan_Daguangba_VillagePopulation_Tabular", "AffectedFeature_Product", "FinalAffectedPoint")
# 可视化参数 products为可视化的数据列表
vis_params = {"products": ["Change_Product", "AffectedFeature_Product"]}
FinalAffectedPoint.styles(vis_params).map()
# import oge
#
# oge.initialize()
# service = oge.Service.initialize()
# cube = service.getCollections(productIDs=["GF_Hainan_Daguangba_NDWI_EO", "Hainan_Daguangba_Village_Vector",
#                                             "Hainan_Daguangba_VillagePopulation_Tabular"],
#                                 datetime=["2016-06-01 00:00:00", "2016-09-01 00:00:00"],
#                                 bbox=[108.90494046724021, 18.753457222586285, 109.18763565740333, 19.0497805438586]
#                                 ).toCube()
# ChangeCube = service.getProcess("Cube.subtract").execute(cube, "GF_Hainan_Daguangba_NDWI_EO", ["2016-08-15 12:00:00", "2016-08-20 12:00:00"], "Change_Product")
# AffectedFeatureCube = service.getProcess("Cube.overlayAnalysis").execute(ChangeCube, "Change_Product", "Hainan_Daguangba_Village_Vector", "AffectedFeature_Product")
# FinalAffectedPoint = service.getProcess("Cube.overlayAnalysis").execute(AffectedFeatureCube, "Hainan_Daguangba_VillagePopulation_Tabular", "AffectedFeature_Product", "FinalAffectedPoint")
# # 可视化参数 products为可视化的数据列表
# vis_params = {"products": ["Change_Product", "AffectedFeature_Product"]}
# FinalAffectedPoint.styles(vis_params).map()