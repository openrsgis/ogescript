# // Load three NAIP quarter quads in the same location, different times.
# var naip2004_2012 = ee.ImageCollection('USDA/NAIP/DOQQ')
#   .filterBounds(ee.Geometry.Point(-71.08841, 42.39823))
#   .filterDate('2004-07-01', '2012-12-31')
#   .select(['R', 'G', 'B']);
#
# // Temporally composite the images with a maximum value function.
# var composite = naip2004_2012.max();
# Map.setCenter(-71.12532, 42.3712, 12);
# Map.addLayer(composite, {}, 'max value composite');

import oge

oge.initialize()
service = oge.Service.initialize("")
collections1 = service.getCoverageCollection("USDA/NAIP/DOQQ")
featureCollection = service.getFeatureCollection("test")
filter1 = oge.Filter.intersect(oge.Geometry.Point(-71.08841, 42.39823))
featureCollection.subCollection(filter1)
collections2 = collections1.subCollection(datetime=['2004-07-01', '2012-12-31'], )
coverage2 = service.getCoverage("LE07_L1TP_ARD_EO", "Red")
coverage3 = service.getProcess("Coverage.add").execute(coverage1, coverage2)
coverage4 = service.getProcess("Coverage.subtract").execute(coverage1, coverage2)
coverage5 = service.getProcess("Coverage.divide").execute(coverage3, coverage4)
coverage6 = service.getProcess("Coverage.binaryzation").execute(coverage5, 0)
vis_params = {'min': 0, 'max': 255}
coverage7 = coverage6.styles(vis_params)
coverage7.map()