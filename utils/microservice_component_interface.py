from accessify import private

class MicroserviceComponentInterface:
    def action(self):
        pass

    @private
    def make_error(self, error_description):
        pass

    @private
    def validate_data(self, **kwargs):
        pass
