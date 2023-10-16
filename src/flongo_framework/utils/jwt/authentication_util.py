import traceback
from typing import Optional, Union, Any

from flask import Response
from flask_jwt_extended import get_jwt, set_access_cookies, set_refresh_cookies, unset_jwt_cookies, verify_jwt_in_request

from ...api.requests.identity import Request_Identity
from ...api.responses.errors.api_error import API_Error
from ..jwt.jwt_manager import App_JWT_Manager

class Authentication_Util:
    ''' Utility for managing application authentication via JWT cookies '''

    @classmethod
    def validate_identity_cookie_role(cls, valid_roles:list[str]) -> Request_Identity:
        ''' Validate the identity passed in the Request being handled has a role
            contained in the list of valid roles passed to the method 
            (if a valid JWT identity cookie is present)

            Returns the identity if one is present
        '''

        current_identity = cls.get_current_identity()
        if not current_identity or not all(role in current_identity.roles for role in valid_roles):
            # User doesn't have required roles; deny access or handle accordingly
            raise API_Error(
                f"Insufficient permissions to access this route. A JWT cookie with one of the following roles is required: {valid_roles}",
                status_code=403,
                stack_trace=traceback.format_exc()
            )
        
        return current_identity
        

    @staticmethod
    def set_identity_cookie(response:Response, _id:str, roles:Optional[Union[str, list[str]]]='') -> Response:
        ''' Sets a JWT identity cookie in the response which will be stored by the client '''
        
        set_access_cookies(response, App_JWT_Manager.create_access_token(_id, roles))
        set_refresh_cookies(response, App_JWT_Manager.create_refresh_token(_id, roles))

        return response
    

    @staticmethod
    def unset_identity_cookie(response:Response) -> Response:
        ''' Unsets the JWT identity cookie in the response which will be purged by the client '''
        
        unset_jwt_cookies(response)
        return response
    

    @staticmethod
    def get_current_identity() -> Optional[Request_Identity]:
        ''' Gets the identity passed in the Request being handled if a valid JWT identity cookie is present '''
        
        verify_jwt_in_request(optional=True)
        if jwt:=get_jwt():
            return Request_Identity.from_dict(jwt)
