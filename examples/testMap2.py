import oge


def Slope(image):
    """A function to compute NDVI."""
    service.getProcess("Coverage.slope").execute(image, 1)
    return service.getProcess("Coverage.slope").execute(image, 1)


oge.initialize()
service = oge.Service.initialize()
demCollection1 = service.getCoverageCollection(productID="ASTER_GDEM_DEM30", bbox=[29.1, 114.1, 29.9, 114.9],
                                               datetime=["2000-01-01 00:00:00", "2000-01-01 00:00:00"])
demCollection2 = demCollection1.map(Slope)
vis_params = {'min': 0, 'max': 255}
demCollection2.styles(vis_params).getMap()
