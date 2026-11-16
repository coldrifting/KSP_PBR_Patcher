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


# noinspection calling-non-callable
def is_debugger_attached():
    # Check if pydevd or pdb is loaded in sys.modules
    get_trace = getattr(sys, 'gettrace', None)
    if get_trace is None:
        return False

    if not callable(get_trace):
        return False

    return get_trace() is not None or 'pydevd' in sys.modules
