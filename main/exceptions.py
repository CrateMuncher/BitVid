

class BitVidException(Exception):
    pass


class ModelSaveException(BitVidException):
    pass

class ValidationException(BitVidException):
    def __init__(self, Errors):

        # Call the base class constructor with the parameters it needs
        Exception.__init__(self, str(Errors[0]))

        # Now for your custom code...
        self.Errors = Errors