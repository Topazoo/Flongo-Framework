from typing import Callable, Optional
from flask import Request, Response
from pymongo.collection import Collection

HandlerMethod = Callable[[Request, dict, Optional[Collection]], Response]
