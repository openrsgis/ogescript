import oge
from . import Cube


class NDWICube(Cube):
    @staticmethod
    def compute(*kwargs):
        oge.initialize()
        service = oge.Service()
        cube = oge.Cube(crs="WGS84", titleSize=1, titlePixel=4000, resample="near",
                        spatialExtent=[108.90494046724021, 18.753457222586285, 109.18763565740333, 19.0497805438586],
                        timeExtent=["2016-06-01 00:00:00", "2016-09-01 00:00:00"])
        cube.add(kwargs["eoCollection"], "LE07_L1TP_ARD_EO")
        # 对cube进行了操作，意味着cube所蕴含的工作流将被改变
        ndwiCube = cube.aggregateDimension(dimension="bands", sourceLabels=[["band4", "band5"]], process="normalize",
                                           targetLabels=["NDVI"])
        binaryCube = ndwiCube.apply(process="binary", context={"threshold": 0})
        changeCube = binaryCube.aggregateTime(inverals=[["2016-08-15 12:00:00", "2016-08-20 12:00:00"]],
                                              process="subtract", labels=["15-20"])
        changeCube.add(kwargs["vectorCollection"], "Hainan_Daguangba_Village_Vector")
        affectedFeatureCube = changeCube.aggregateDimension(dimension="product", sourceLabels=[
            ["LE07_L1TP_ARD_EO", "Hainan_Daguangba_Village_Vector"]], process="overlay",
                                                            targetLabels=["AffectedFeature_Product"])
        changeCube.add(kwargs["tabularCollection"], "Hainan_Daguangba_Village_Vector")
        affectedPopular = affectedFeatureCube.aggregateDimension(dimension="product", sourceLabels=[
            ["AffectedFeature_Product", "Hainan_Daguangba_VillagePopulation_Tabular"]], process="overlay",
                                                                 targetLabels=["FinalAffectedPoint"])
