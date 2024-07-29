import oge.mapclient

oge.initialize()
image = oge.Image("image")
image1 = image.select("image1")
image2 = image.select("image2")
image3 = image1.add(image2)
image4 = image1.subtract(image2)
image5 = image3.divide(image4)
oge.mapclient.addToMap(image5)
