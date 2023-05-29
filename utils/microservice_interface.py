from accessify import private

class MicroserviceInterface:
    @private
    def configure(self, **configs):
        pass

    @private
    def add_endpoint(self, endpoint, endpoint_name, handler, methods, *args, **kwargs):
        pass

    def run(self, **kwargs):
        pass