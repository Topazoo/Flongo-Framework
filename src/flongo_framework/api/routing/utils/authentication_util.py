import traceback
from typing import Optional, Union

from flask import Response
from flask_jwt_extended import get_jwt, verify_jwt_in_request

from ...requests.identity import Request_Identity
from ...responses.errors.api_error import API_Error
from ....utils.jwt.jwt_manager import App_JWT_Manager

class Authentication_Util:
    ''' Utility for managing application authentication via JWT cookies '''

    @classmethod
    def validate_identity_cookie_role(cls, valid_roles:list[str]) -> Request_Identity:
        ''' Validate the identity passed in the Request being handled has a role
            contained in the list of valid roles passed to the method 
            (if a valid JWT identity cookie is present)

            Returns the identity if one is present
        '''

        error_prefix = "Insufficient permissions to access this route."
        if not (current_identity:=cls.get_current_identity()):
            # No JWT Identity was passed in the request
            raise API_Error(
                f"{error_prefix} A JWT cookie is required.",
                status_code=401,
                stack_trace=traceback.format_exc()
            )
          
        if not any(role in current_identity.roles for role in valid_roles):
            # A JWT Identity was passed in the request but it does not have the right permissions
            raise API_Error(
                f"{error_prefix} A JWT cookie with one of the following roles is required: {valid_roles}",
                status_code=403,
                stack_trace=traceback.format_exc()
            )
        
        return current_identity
        

    @classmethod
    def set_identity_cookies(cls, response:Response, _id:str, roles:Optional[Union[str, list[str]]]='') -> Response:
        ''' Sets a JWT identity cookie in the response which will be stored by the client '''

        return App_JWT_Manager.set_identity_cookies(response, _id, roles)
        

    @classmethod
    def unset_identity_cookies(cls, response:Response) -> Response:
        ''' Unsets the JWT identity cookie in the response which will be purged by the client '''
        
        return App_JWT_Manager.unset_identity_cookies(response)
    

    @staticmethod
    def get_current_identity() -> Optional[Request_Identity]:
        ''' Gets the identity passed in the Request being handled if a valid JWT identity cookie is present '''
        
        verify_jwt_in_request(optional=True)
        if jwt:=get_jwt():
            return Request_Identity.from_dict(jwt)
