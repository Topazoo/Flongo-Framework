from typing import Optional, Union

class DatabaseError(Exception):
    ''' An error thrown while handling a database operation.
        It contains a message and optional stacktrace
    '''

    def __init__(self,
                 message:str,
                 code:Optional[int] = None, 
                 data:Optional[dict] = None, 
                 stack_trace:Union[str, None] = None
        ):
        super(Exception, self).__init__(message)
        
        self.message = message
        self.code = code
        self.data = data or {}
        self.stack_trace = stack_trace


    def set_stack_strace(self, stack_trace:str):
        self.stack_trace = stack_trace
