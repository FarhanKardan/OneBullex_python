class OneBullExException(Exception):
    pass

class OneBullExAPIException(OneBullExException):
    def __init__(self, message, code=None):
        super().__init__(message)
        self.code = code

class OneBullExRequestException(OneBullExException):
    pass
