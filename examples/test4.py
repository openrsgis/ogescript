
import oge
import oge.mapclient

oge.initialize()
image_params1 = {"productName": "LE07_L1TP_ARD_EO", "measurementName": "Near-Infrared",
                 "geom": (113.054, 29.8, 114.588, 30.774)}
image_params2 = {"productName": "LE07_L1TP_ARD_EO", "measurementName": "Red", "geom": (113.054, 29.8, 114.588, 30.774)}
image1 = oge.Image(image_params1)
image2 = oge.Image(image_params2)
image3 = image1.subtract(image2)
image4 = image1.add(image2)
image5 = image3.divide(image4)
image6 = image5.gte(106)
oge.mapclient.addToMap(image6)