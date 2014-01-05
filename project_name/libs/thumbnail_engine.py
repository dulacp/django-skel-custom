from django.conf import settings

# from pilkit.processors import ProcessorPipeline, DominantColorOverlay, ColorOverlay
from sorl.thumbnail.engines.pil_engine import Engine as PILEngine


class CustomPILEngineMixin(object):
    pass

class Engine(CustomPILEngineMixin, PILEngine):
    pass
