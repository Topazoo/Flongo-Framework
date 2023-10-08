from typing import Union

class Request_Handling_Error(Exception):
    ''' An error thrown while handling an API call.
        it contains a message, status code and optional
        stacktrace
    '''
    def __init__(self,
                 method:str,
                 message:str, 
                 status_code:int = 500, 
                 stack_trace:Union[str, None] = None
        ):

        self.method = method
        self.message = message
        self.status_code = status_code
        self.stack_trace = stack_trace


    def __str__(self) -> str:
        base_str = f"[{self.method.upper()}] ERROR {self.status_code or '500'}: {self.message}"
        if self.stack_trace:
            base_str += f' | STACK TRACE: {self.stack_trace}'

        return base_str
