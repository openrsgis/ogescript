import oge
oge.initialize()
service = oge.Service.initialize()
GFCollection = service.getCoverageCollection(productID="GF2", bbox=[101.22, 25.14, 101.23, 25.15])
farmlandImage = service.getProcess("CoverageCollection.deepLearning").execute(GFCollection, "farmland")
vis_params = {'min': 0, 'max': 255}
farmlandImage.styles(vis_params).getMap()


