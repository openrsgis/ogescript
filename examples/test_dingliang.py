import oge

oge.initialize()
service = oge.Service.initialize()
# productID随便了，后端数据是定死的
modisCollection = service.getCoverageCollection(productID="MOD13Q1_061")
changShaFeature = service.getFeatureCollection("ChangSha")

#################案例一##########################
# # 计算植被/水体指数 2018年 第一季度
indexCollection = modisCollection.calVegIndex("2018", "1")
# 用长沙的矢量裁剪
indexResultCollection = indexCollection.calCrop(changShaFeature, "2018", "1", "vegIndex")
indexResultCollection.styles({}).getMap()

# #################案例二##########################
# # # 计算植被覆盖率 2018年 第一季度
# fovCollection = modisCollection.calVegCoverage("2018", "1")
# resultCollection = fovCollection.calCrop(changShaFeature, "2018", "1", "vegCoverage")
# resultCollection.styles({}).getMap()

# #################案例二##########################
# 计算植被生产力 2018年 第一季度
nppCoverage = indexResultCollection.calNPP("2018", "1")
nppCoverage.styles({}).getMap()