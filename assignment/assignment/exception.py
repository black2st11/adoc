from rest_framework.response import Response
from rest_framework.views import exception_handler


class CustomException(Exception):
    def __init__(self, message, status_code=400, code=None):
        self.message = message
        self.status_code = status_code
        self.code = code
        super().__init__(self.message)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if not response:
        if isinstance(exc, CustomException):
            return Response(
                {"message": exc.message, "code": exc.code}, status=exc.status_code
            )
        raise exc
        return Response({"message": "Internal Server Error"}, status=500)
    return response
