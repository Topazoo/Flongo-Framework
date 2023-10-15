from ...config.enums.http_methods import HTTP_METHODS
from ...utils.requests import JSON_Schema_Validator

from flask import Request
from typing import Any, Optional

class Route_Schema:
    ''' Base class that allows JSONSchemas to be bound
        to specific HTTP methods like GET or POST

        Used in conjuction with a Route to hold JSONSchemas
        for each method for request or response validation
    '''

    # Holds a reference of all passed schemas
    def __init__(self, **method_schemas:dict[str, Any]):
        self.schemas = {}
        for method, schema in method_schemas.items():
            normalized_method = method.upper()
            # Ensure the method is a valid HTTP method
            if normalized_method.lower() not in HTTP_METHODS:
                raise ValueError(f"Schema: [{normalized_method}] is not a valid HTTP method.")

            # Create a property for the HTTP method passed
            # with the dictionary containing the schema
            setattr(self, normalized_method, schema)
            self.schemas[normalized_method] = schema
    

    def get_schemas(self) -> dict[str, dict[str, Any]]:
        ''' Returns all schemas stored by this class
        '''

        return self.schemas
    

    def get_schema(self, method:str) -> Optional[dict[str, Any]]:
        ''' Returns a schemas stored by this class
        '''

        return self.get_schemas().get(method)
    

    def validate_schema(self, request:Request, payload:dict, is_response_schema=False) -> bool:
        ''' Validate the request payload against a JSONSchema if one was supplied
            Returns True if a schema was validated, False if one was not and throws
            an exception if schema validation failed 
        '''

        method = request.method.upper()
        if schema:=self.get_schema(method):
            validator = JSON_Schema_Validator(schema, request.url_root, method, is_response_schema)
            validator.validate_request(payload)

            return True
        
        return False
