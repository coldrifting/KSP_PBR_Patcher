import sys


class CustomException(BaseException):
    def __init__(self, message: str):
        self.message = message
        self.type_name = type(self).__name__

class ArgumentException(CustomException):
    pass

class AttributeInvalidError(CustomException):
    pass

class AttributeNotFoundError(CustomException):
    pass

class AttributeAlreadyExistsError(CustomException):
    pass

def is_debugger_attached():
    # Check if pydevd or pdb is loaded in sys.modules
    gettrace = getattr(sys, 'gettrace', None)
    if gettrace is None:
        return False
    else:
        return gettrace() is not None or 'pydevd' in sys.modules
