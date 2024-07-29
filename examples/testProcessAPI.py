import oge

oge.initialize()
service = oge.Service.initialize("http//127.0.0.1:5000/")
# dem = service.getCoverage("DEMProduct", "dem")
slopeDem = service.getProcess("hello-world").execute(name="wkx", message="hello").getCoverage("echo")

# slopeDem = service.process("Slope", dem, 1.0)
vis_params = {'min': 0, 'max': 255}
slopeDem.styles(vis_params).getMap()