from jsonschema import ValidationError, validate

from ...api.errors.schema_validation_error import SchemaValidationError

class JSON_Schema_Validator:
    ''' Base class for validating a JSONSchema against
        a passed request payload
    '''

    def __init__(self, json_schema:dict[str, dict], url:str='', method:str='', is_response_schema:bool=False) -> None:
        self.url = url
        self.method = method
        self.json_schema = json_schema
        self.is_response_schema = is_response_schema


    def validate_request(self, payload:dict):
        ''' Validate a request payload against the provided schema '''

        try:
            validate(payload, self.json_schema)
        except ValidationError as e:
            raise SchemaValidationError(
                self.url,
                self.method,
                e.message,
                self.json_schema,
                is_response_schema=self.is_response_schema
            )
