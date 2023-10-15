from ...config.enums.base.base_str_enum import BaseStrEnum

class HTTP_METHODS(BaseStrEnum):
    """ HTTP methods supported by the application """

    OPTIONS = "options"
    GET = "get"
    POST = "post"
    PUT = "put"
    PATCH = "patch"
    DELETE = "delete"
