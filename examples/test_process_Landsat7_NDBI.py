import oge

oge.initialize()
service = oge.Service.initialize()
imageCollection = service.getCoverageCollection(productID="LE07_L1TP_C01_T1", bbox=[113.054, 29.8, 114.588, 30.774],
                                                 datetime=["2014-01-01 00:00:00", "2016-12-31 00:00:00"])
imageCollection.map()
imageCollection_NearInrared = imageCollection.subCollection(filter=oge.Filter([oge.Filter.equals("crs", "EPSG:32649"), oge.Filter.equals("measurementName", "Near-Infrared")]))
imageCollection_SWIR1 = imageCollection.subCollection(filter=oge.Filter([oge.Filter.equals("crs", "EPSG:32649"), oge.Filter.equals("measurementName", "SWIR 1")]))
imageNearInrared = service.getProcess("CoverageCollection.mosaic").execute(imageCollection_NearInrared, "min")
imageSWIR1 = service.getProcess("CoverageCollection.mosaic").execute(imageCollection_SWIR1, "min")
image3 = service.getProcess("Coverage.subtract").execute(imageNearInrared, imageSWIR1)
image4 = service.getProcess("Coverage.add").execute(imageNearInrared, imageSWIR1)
image5 = service.getProcess("Coverage.divide").execute(image3, image4)
image6 = service.getProcess("Coverage.binarization").execute(image5, 0)
vis_params = {'min': 0, 'max': 255}
image6.styles(vis_params).map()

