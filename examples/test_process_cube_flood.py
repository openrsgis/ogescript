import oge

oge.initialize()
service = oge.Service.initialize()
cube = service.getCollections(productIDs=["LE07_L1TP_ARD_EO", "Hainan_Daguangba_Village_Vector",
                                          "Hainan_Daguangba_VillagePopulation_Tabular"],
                              datetime=["2016-06-01 00:00:00", "2016-09-01 00:00:00"],
                              bbox=[108.90494046724021, 18.753457222586285, 109.18763565740333, 19.0497805438586]
                              ).toCube()
NDWICube = service.getProcess("Cube.NDWI").execute(cube, "LE07_L1TP_ARD_EO", "NDWI_Product")
BinaryCube = service.getProcess("Cube.binarization").execute(NDWICube, "NDWI_Product", 0, "Binarization_Product")
ChangeCube = service.getProcess("Cube.subtract").execute(
    BinaryCube, "Binarization_Product", ["2016-08-15 12:00:00", "2016-08-20 12:00:00"], "Change_Product")
AffectedFeatureCube = service.getProcess("Cube.overlayAnalysis").execute(
    ChangeCube, "Change_Product", "Hainan_Daguangba_Village_Vector", "AffectedFeature_Product")
FinalAffectedPoint = service.getProcess("Cube.conjointAnalysis").execute(
    AffectedFeatureCube, "AffectedFeature_Product", "Hainan_Daguangba_VillagePopulation_Tabular", "FinalAffectedPoint")
# 可视化参数 products为可视化的数据列表
vis_params = {"products": ["Change_Product", "FinalAffectedPoint"]}
FinalAffectedPoint.styles(vis_params).map()
