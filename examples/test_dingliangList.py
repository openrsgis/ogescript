import oge

oge.initialize()
service = oge.Service.initialize()
# productID随便了，后端数据是定死的
modisCollection = service.getCoverageCollection(productID="MOD13Q1_061")
changShaFeature = service.getFeatureCollection("ChangSha")
nppList = []
fovList = []
for i in range(1, 5):
    indexCollection = modisCollection.calVegIndex("2018", str(i))
    indexResultCollection = indexCollection.calCrop(changShaFeature, "2018", str(i), "vegIndex")
    nppCoverage = indexResultCollection.calNPP("2018", str(i))
    nppList.append(nppCoverage)
    fovCollection = modisCollection.calVegCoverage("2018",  str(i))
    fovResultCollection = fovCollection.calCrop(changShaFeature, "2018",  str(i), "vegCoverage")
    fovList.append(fovResultCollection)

nppCollection = oge.CoverageCollection(nppList)
fovCollection = oge.CoverageCollection(fovList)
vei = fovCollection.calVEI(nppCollection, "2018")
vei.styles({}).getMap()