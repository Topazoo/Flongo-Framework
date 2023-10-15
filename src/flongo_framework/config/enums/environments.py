from ...config.enums.base.base_str_enum import BaseStrEnum

class ENVIRONMENTS(BaseStrEnum):
    """ Development environments levels supported by the application """

    DEVELOPMENT = "development"
    QA = "qa"
    SANDBOX = "sandbox"
    STAGING = "staging"
    PRODUCTION = "production"
