from ...utils.logging.loggers.routing import RoutingLogger
from ...config.enums.http_methods import HTTP_METHODS

from flask import Request
from typing import Any, Optional

class Route_Transformer:
    ''' Base class that allows payload data to be transformed by
        a given lambda for each HTTP method like GET or POST

        Used in conjuction with a Route to hold Transformers
        for each method to manipulate the received payload
    '''

    # Holds a reference of all passed transformers
    def __init__(self, **method_transformers:dict[str, Any]):
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
    

    def get_transformers(self) -> dict[str, dict[str, Any]]:
        ''' Returns all transformers stored by this class
        '''

        return self.transformers
    

    def get_transformer(self, method:str) -> Optional[dict[str, Any]]:
        ''' Returns a transformer stored by this class
        '''

        return self.get_transformers().get(method)
    

    def transform(self, request:Request, payload:dict, logger:Optional[RoutingLogger]=None) -> dict:
        ''' Transforms the request payload against a transformer if one is supplied
            Returns the transformed payload 
        '''

        method = request.method.upper()
        if transformer:=self.get_transformer(method):
            for field, func in transformer.items():
                if field in payload:
                    transformed_data = func(payload[field])
                    if logger:
                        logger.debug(f'* Transformed payload data for field [{field}]: {payload[field]} -> {transformed_data}')

                    payload[field] = transformed_data

        return payload
