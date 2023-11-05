from .....utils.logging.loggers.routing import RoutingLogger
from .....config.enums.http_methods import HTTP_METHODS
from .field_transformer import Field_Transformer

from flask import Request
from typing import Optional

class Route_Transformer:
    ''' Base class that allows payload data to be transformed by
        a given lambda for each HTTP method like GET or POST

        Used in conjuction with a Route to hold Transformers
        for each method to manipulate the received payload
    '''

    # Holds a reference of all passed transformers
    def __init__(self, **method_transformers:list[Field_Transformer]):
        self.transformers = {}
        for method, transformer in method_transformers.items():
            normalized_method = method.upper()
            # Ensure the method is a valid HTTP method
            if normalized_method.lower() not in HTTP_METHODS:
                raise ValueError(f"Transformer: [{normalized_method}] is not a valid HTTP method.")

            # Create a property for the HTTP method passed
            # with the dictionary containing the transformer
            setattr(self, normalized_method, transformer)
            self.transformers[normalized_method] = transformer
    

    def get_field_transformers_for_methods(self) -> dict[str, list[Field_Transformer]]:
        ''' Returns all transformers stored by this class
        '''

        return self.transformers
    

    def get_field_transformers(self, method:str) -> Optional[list[Field_Transformer]]:
        ''' Returns a transformer stored by this class
        '''

        return self.get_field_transformers_for_methods().get(method)
    

    def transform(self, request:Request, payload:dict, logger:Optional[RoutingLogger]=None) -> dict:
        ''' Transforms the request payload against a transformer if one is supplied
            Returns the transformed payload 
        '''

        method = request.method.upper()
        if field_transformers:=self.get_field_transformers(method):
            for field_transformer in field_transformers:
                # Function is to insert a default
                if field_transformer.is_default:
                    payload[field_transformer.field_name] = field_transformer.transform_func()
                    if logger:
                        logger.debug(f'* Transformer created default payload data for field [{field_transformer.field_name}] -> {payload[field_transformer.field_name]}')
                
                # Function is to transform data
                elif field_transformer.field_name in payload:
                    payload[field_transformer.field_name] = field_transformer.transform_func(payload[field_transformer.field_name])
                    # Remove if the transformer set the data to None
                    if payload[field_transformer.field_name] == None:
                        del payload[field_transformer.field_name]
                        if logger:
                            logger.debug(f'* Transformer removed payload data for field [{field_transformer.field_name}]')
                    elif logger:
                        logger.debug(f'* Transformer modified payload data for field [{field_transformer.field_name}] -> {payload[field_transformer.field_name]}')
                        
        return payload
