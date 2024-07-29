import oge

oge.initialize()
service = oge.Service.initialize("https://maps.gnosis.earth/ogcapi/")
sentinel2 = service.getCoverage("sentinel2", "sentinel2-l2a")
# sentinel2_1 = sentinel2.auto("sssss")
# slopeDem = service.getProcess("hello-world").execute(name="wkx", message="hello").getCoverage("echo")

# slopeDem = service.process("Slope", dem, 1.0)
vis_params = {'min': 0, 'max': 255}
sentinel2.styles(vis_params).getMap()