from typing import Optional

class SchemaValidationError(Exception):
    ''' An error thrown when an incoming request payload
        does not adhere to the JSON schema assigned to
        the endpoint 
    '''
    def __init__(self,
                 url:str,
                 method:str,
                 raw_path:Optional[str],
                 json_schema:dict,
                 status_code:int = 400, 
        ):

        self.url = url
        self.method = method
        self.raw_path = raw_path
        self.json_schema = json_schema
        self.status_code = status_code


    def __str__(self) -> str:
        return f"[{self.method.upper()}] SCHEMA VALIDATION ERROR {self.status_code}"

    def to_json(self, include_schema:bool = False) -> dict:
        ''' Creates a JSON payload of this data optionall including
            the schema `include_schema` is True
        '''

        return {
            'error': str(self),
            'url': self.url,
            'method': self.method.upper(),
            'path': self.raw_path,
            **({} if not include_schema else {'json_schema': self.json_schema})
        }
