import oge

oge.initialize()
# 获取collections
collections = oge.Service.collections(datetime="2019-10-12T07:20:50.52Z/2019-11-12T07:20:50.52Z",
                                      bbox=[160.6, -55.95, -170, -25.89], bbox_crs="WGS84")
# 获取feature collection
feature_collection = collections.collection("Building").getFeatureCollection()
coverage_collection = collections.collection("Landsat8").getCoverageCollection()
# 获取coverage collection
feature_test = feature_collection.getFeature("Buildings/whuhan/wuchang")
coverage_test = coverage_collection.getCoverage("Landsat8/8c")
# 计算NDWI
NDWI = oge.Service.process("normalizedDifference").execute(coverage_test, ["green", "blue"])
# 缓冲区计算
feature_buffer = oge.Service.process("buffer").execute(feature_test, 12)
vis_params = {"bands": ["green", "blue"]}
# 可视化 返回JSON
json1 = NDWI.styles(vis_params).map()
json2 = coverage_collection.styles(vis_params).map()
json3 = feature_collection.styles(vis_params).map()
json4 = feature_test.styles(vis_params).map()
json5 = feature_buffer.map()
print(json1)
print(json2)
print(json3)
print(json4)
print(json5)
