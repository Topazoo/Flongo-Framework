from typing import Optional

class SchemaValidationError(Exception):
    ''' An error thrown when an incoming request payload
        does not adhere to the JSON schema assigned to
        the endpoint 
    '''
    def __init__(self,
                 url:str,
                 method:str,
                 message:str,
                 json_schema:dict,
                 status_code:int = 400,
                 is_response_schema:bool = False
        ):

        self.url = url
        self.method = method
        self.message = message
        self.json_schema = json_schema
        self.status_code = status_code
        self.is_response_schema = is_response_schema


    def get_data(self, include_schema:Optional[bool] = False) -> dict:
        ''' Creates a map of this data optionall including
            the schema `include_schema` is True
        '''

        return {
            'url': self.url,
            'method': self.method,
            'is_response_schema': self.is_response_schema,
            **({} if not include_schema else {'method_schema': self.json_schema})
        }
