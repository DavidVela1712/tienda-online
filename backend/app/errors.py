class AppError(Exception):
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class ValidationError(AppError):
    def __init__(self, message):
        super().__init__(message, 400)

class NotFoundError(AppError):
    def __init__(self, message):
        super().__init__(message, 404)

class ForbiddenError(AppError):
    def __init__(self, message):
        super().__init__(message, 403)