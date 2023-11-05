from typing import Callable

class Field_Transformer:
    ''' Class to hold transformer information for a specific field
    '''

    def __init__(self, field_name:str, transform_func:Callable, is_default:bool=False) -> None:
        self.field_name = field_name
        self.transform_func = transform_func
        self.is_default = is_default
