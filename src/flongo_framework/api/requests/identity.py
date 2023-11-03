from typing import Optional

class Request_Identity:
    ''' 
        Base class that wraps Flask JWT's identity dictionary
    '''

    def __init__(
            self,
            _id:str,
            fresh:bool=False,
            iat:int=0,
            jti:str='',
            type:str='access',
            nbf:int=0,
            csrf:str='',
            exp:int=0,
            roles:Optional[list[str]]=None
        ) -> None:
        
        self._id = _id
        self.fresh = fresh
        self.iat = iat
        self.jti = jti
        self.type = type,
        self.nbf = nbf
        self.csrf = csrf
        self.exp = exp
        self.roles = roles or []


    @classmethod
    def from_dict(cls, data:dict) -> "Request_Identity":
        return Request_Identity(data.pop("sub"), **data)


    def to_dict(self) -> dict:
        return {
            "sub": self._id,
            "fresh": self.fresh,
            "iat": self.iat,
            "jti": self.jti,
            "type": self.type,
            "nbf": self.nbf,
            "exp": self.exp,
            "roles": self.roles,
            "csrf": self.csrf
        }
