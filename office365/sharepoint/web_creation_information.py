from office365.runtime.client_value_object import ClientValueObject


class WebCreationInformation(ClientValueObject):
    """Represents metadata about site creation."""

    def __init__(self):
        super(WebCreationInformation, self).__init__()
        self.Title = None
        self.Url = None

    @property
    def tagName(self):
        return "parameters"

    @property
    def typeName(self):
        return "SP.WebCreationInformation"
