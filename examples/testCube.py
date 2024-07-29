import oge

oge.initialize()

# initialize the OGC API endpoint
service = oge.Service()
sentinelCube = service.getCube(cubeId=3, products="[LC08_L2SP_C02_T1]", bands="[SR_B3,SR_B5]", time="[2023-01-10 00:00:00,2023-01-17 00:00:00]",
                               extent="[114.16,30.47,114.47,30.69]", tms="WebMercatorQuad", resolution=30)
ndviCube = service.getProcess("Cube.NDVI").execute(sentinelCube, ["SR_B3", "Landsat 8"], ["SR_B3", "Landsat 8"])
vis_params = {"bands": "[ndvi]", "min": "0", "max": "500"}
# styledCube = ndviCube.styles(vis_params).map()
# print(sentinelCube)
print(ndviCube)


# # ndviCube = service.getProcess("Cube.normalize").execute(sentinelCube, "bands", ["B8", "B3"])
# meanNdviCube = service.getProcess("Cube.aggregate").execute(ndviCube, "time", "mean")
# # 地图可视化
# vis_params = {'min': -1, 'max': 1, 'palette': ["GoldenRod", "Gold", "LightGreen", "LimeGreen", "Green"]}
# meanNdviCube.styles(vis_params).getMap("ndvi_mean")