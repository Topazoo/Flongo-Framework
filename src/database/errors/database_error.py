from typing import Optional, Union

class DatabaseError(Exception):
    ''' An error thrown while handling a database operation.
        It contains a message and optional stacktrace
    '''

    def __init__(self,
                 message:str,
                 data:Optional[dict] = None, 
                 stack_trace:Union[str, None] = None
        ):

        self.message = message
        self.data = data or {}
        self.stack_trace = stack_trace
