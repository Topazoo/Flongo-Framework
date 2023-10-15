from ...config.enums.base.base_str_enum import BaseStrEnum

class MONGODB_INDEX_TYPES(BaseStrEnum):
    """ Types of indices supported for MongoDB """

    TEXT = "text"
    COMPOUND = "compound"
    STANDARD = "standard"
