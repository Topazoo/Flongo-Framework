from datetime import timedelta
import time
import traceback
from typing import Optional, Union
from flask_jwt_extended import JWTManager, get_jwt, get_jwt_identity, \
    set_access_cookies, set_refresh_cookies, verify_jwt_in_request, unset_jwt_cookies
from flask import Flask, Response
from src.flongo_framework.api.responses.errors.api_error import API_Error

from src.flongo_framework.config.settings.jwt_settings import JWT_Settings
import flask_jwt_extended

class App_JWT_Manager(JWTManager):
    ''' Utilities for managing JWT for the application '''

    def __init__(self, app:Flask, settings:JWT_Settings, add_context_processor:bool=False) -> None:
        self.settings = settings

        super().__init__(app, add_context_processor)
        self._configure_app_settings(app)


    def _configure_app_settings(self, app:Flask):
        ''' Configure the Flask app config for JWT '''

        app.config['JWT_SECRET_KEY'] = self.settings.secret_key
        app.config['JWT_ACCESS_TOKEN_EXPIRES'] = self.settings.access_token_expiration_secs
        app.config['JWT_REFRESH_TOKEN_EXPIRES'] = self.settings.refresh_token_expiration_secs
        app.config['JWT_COOKIE_SECURE'] = self.settings.only_allow_https
        app.config['JWT_COOKIE_CSRF_PROTECT'] = self.settings.enable_csrf_protection
        app.config['JWT_CSRF_IN_COOKIES'] = self.settings.enable_csrf_protection

        app.config['JWT_TOKEN_LOCATION'] = ['cookies']


    def _configure_app_middleware(self, app:Flask):
        ''' Configure request and response interceptors for JWT handling '''

        # Add token refresh handler for silent refresh
        app.after_request(self.renew_token_middleware)


    def renew_token_middleware(self, response:Response):
        current_identity = get_jwt_identity()
        if current_identity:
            token_exp = current_identity['exp']
            # Renew if the token will expire in X seconds
            if token_exp - time.time() < self.settings.refresh_access_token_within_secs:
                new_access_token = flask_jwt_extended.create_access_token(
                    identity=current_identity, 
                    expires_delta=timedelta(seconds=self.settings.access_token_expiration_secs or 300)
                )
                set_access_cookies(response, new_access_token)

        return response
    

    @staticmethod
    def _normalize_roles(roles:Optional[Union[str, list[str]]]='') -> list[str]:
        if not roles:
            roles = []

        if not isinstance(roles, list):
            roles = [roles]

        return roles
    

    @classmethod
    def create_access_token(cls, _id:str, roles:Optional[Union[str, list[str]]]=''):
        return flask_jwt_extended.create_access_token(
            identity=_id, 
            additional_claims={'roles': cls._normalize_roles(roles)}
        )
    

    @classmethod
    def create_refresh_token(cls, _id:str, roles:Optional[Union[str, list[str]]]=''):
        return flask_jwt_extended.create_access_token(
            identity=_id, 
            additional_claims={'roles': cls._normalize_roles(roles)}
        )
    

    @classmethod
    def create_tokens(cls, _id:str, roles:Optional[Union[str, list[str]]]=''):
        return cls.create_access_token(_id, roles), cls.create_refresh_token(_id, roles)


    @classmethod
    def validate_jwt_roles(cls, required_roles:list[str]):
        current_identity = cls.get_current_jwt()
        if not current_identity or not all(role in current_identity.get('roles', []) for role in required_roles):
            # User doesn't have required roles; deny access or handle accordingly
            raise API_Error(
                f"Insufficient permissions to access this route. A JWT token with one of the following roles is required: {required_roles}",
                status_code=403,
                stack_trace=traceback.format_exc()
            )
        

    @classmethod
    def add_response_jwt(cls, response:Response, _id:str, roles:Optional[Union[str, list[str]]]='') -> Response:
        set_access_cookies(response, cls.create_access_token(_id, roles))
        set_refresh_cookies(response, cls.create_refresh_token(_id, roles))

        return response
    

    @classmethod
    def remove_response_jwt(cls, response:Response) -> Response:
        unset_jwt_cookies(response)

        return response
    

    @classmethod
    def get_current_jwt(cls):
        ''' Gets the current JWT data from Flask context '''
        
        verify_jwt_in_request(optional=True)
        return get_jwt()
