import oge
import oge.mapclient

oge.initialize()
service = oge.Service.initialize()
# productID随便了，后端数据是定死的
############################  1  #####################################
# temperature2006 = service.getTable("temperature2006")
# inputStation = service.getFeatureCollection("climateStation")
# resultTable = service.process("Algorithm.hargreaves", temperature2006, inputStation, "2006-01-01 00:00:00", "2006-12-31 00:00:00", 86400)
# resultTable.getDownLoadUrl("csv", "fileName1")

############################  2  #####################################
# TopoIndex = service.getTable("TopoIndex")
# precipEvapFile = service.getTable("precipEvapFile")
# resultTable = service.process("Algorithm.topmodel", 9.66, 90, 240000, 3, 124800, "2006-01-01 12:00:00", "2006-12-31 12:00:00", 86400, TopoIndex, precipEvapFile)
# resultTable.getDownLoadUrl("csv", "fileName2")

############################  3  #####################################
inp = service.getTable("Example2-Post")
resultTable = service.process("Algorithm.swmm", inp)
oge.mapclient.centerMap(115.21, 24.17, 1)
resultTable.getMap()
# resultTable.getDownLoadUrl("csv", "fileName3")