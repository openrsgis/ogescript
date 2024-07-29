import oge
# 初始化
oge.initialize()
service = oge.Service.initialize()

csv = service.getSheet("myData/test1.csv")
csv_sel = service.getProcess("Sheet.filterByHeader").execute(csv, "age", "25")
csv_slice = service.getProcess("Sheet.slice").execute(csv_sel, "true", 1,3)
cell_v = service.getProcess("Sheet.getcellValue").execute(csv_slice, 1, 2)
# csv.log("csv")
# csv_sel.log("csv_sel")
# csv_slice.log("csv_slice")
cell_v.log("cell_v")