import oge
# 初始化
oge.initialize()
service = oge.Service.initialize()

csv = service.getProcess("Sheet.getCsv").execute("myData/test1.csv")
csv.log("csv")