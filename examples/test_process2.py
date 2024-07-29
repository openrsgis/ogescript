import oge
import oge.mapclient

oge.initialize()
# 初始化Service
# service = oge.Service.initialize("http//localhost:8080")
service = oge.Service()
# getCollections
collections_test = service.getCollections()
collection_test = service.getCollection("test_collection_id")
item_test = collection_test.getItem("id")
item_type = item_test.getItemType()
print(item_test.map())
# featureItem = item_test.toFeature()
# coverageItem = item_test.toCoverage()
# print(coverageItem.map())
a = 1
# processes_list = service.getProcesses()
# process_test = processes_list.getProcess("NDWI")
# imageLoadProcess = service.getProcess("Image.load")
# image1 = imageLoadProcess.execute("test1")
# image2 = imageLoadProcess.execute("test2")
# imageAddProcess = service.getProcess("Image.add")
# image3 = imageAddProcess.execute(image1, image2)
# imageSubtractProcess = service.getProcess("Image.subtract")
# image4 = imageSubtractProcess.execute(image1, image2)
# imageDivideProcess = service.getProcess("Image.divide")
# image5 = imageDivideProcess.execute(image3, image4)

# process_test.getInfo()
# result = process_test.execute(collection_test, ["green", "blue"])
# vis_params = {"products": ["ChangeDetection", "AffectedFeature"]}
# oge.mapclient.addToMap(coverageItem, vis_params)
# oge.mapclient.addToMap(image5, vis_params)
# a = 1
# collection_test = collections_test.getCollection("Landsat7")
# collection_test_immediate = collections_test.getCollection("Landsat7", immediate=True)
# processes_test = service.getProcesses("image")
# processe_test = processes_test.getProcess("NDWI")
# direct_process = oge.Process("normalizedDifference")
# # NDWI = oge.Process("normalizedDifference").execute(coverage_test, ["green", "blue"])
# a = 1
