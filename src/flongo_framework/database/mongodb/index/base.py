from typing import Optional
from ....config.enums.mongodb_index_types import MONGODB_INDEX_TYPES

class MongoDB_Index:
    ''' Stores MongoDB index information '''

    def __init__(self, 
            collection_name:str, 
            field_name:str, 
            order:int=1, 
            properties:Optional[dict]=None, 
            compound_index:Optional["MongoDB_Index"]=None, 
            is_text:bool=False
        ):

        self.collection_name = collection_name
        self.field_name = field_name
        self.order = order
        self.properties = properties or {}
        self.compound_index = compound_index
        self.is_text = is_text

    @property
    def index_type(self) -> str:
        ''' Get the type of index '''

        if self.is_text:
            return MONGODB_INDEX_TYPES.TEXT
        elif self.compound_index:
            return MONGODB_INDEX_TYPES.COMPOUND
        else:
            return MONGODB_INDEX_TYPES.STANDARD
