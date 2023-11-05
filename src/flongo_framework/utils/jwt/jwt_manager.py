import time
import traceback
from typing import Optional, Union
from flask_jwt_extended import JWTManager, get_jwt, set_access_cookies, set_refresh_cookies, unset_jwt_cookies, verify_jwt_in_request
from flask import Flask, Response, request

from ...config.settings.app_settings import App_Settings
from ...utils.logging.loggers.app import ApplicationLogger
from ...config.settings.jwt_settings import JWT_Settings
from ...api.responses.errors.api_error import API_Error
import flask_jwt_extended
from jwt.exceptions import ExpiredSignatureError
from flask_jwt_extended.exceptions import CSRFError

class App_JWT_Manager(JWTManager):
    ''' Utilities for managing JWT for the application '''

    APP_IDENTITY_COOKIE = "identity_cookie"

    def __init__(self, app:Flask, settings:JWT_Settings, add_context_processor:bool=False) -> None:
        self.settings = settings

        super().__init__(app, add_context_processor)
        self._configure_app_settings(app)
        self._configure_app_middleware(app)


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
        if request.method == 'OPTIONS':
            return response
        
        try:
            verify_jwt_in_request(optional=True)
            current_identity = get_jwt()
            if current_identity:
                token_exp = current_identity['exp']
                # Renew if the token will expire in X seconds
                if token_exp - time.time() < self.settings.refresh_access_token_within_secs:
                    self.set_access_cookies(response, current_identity['sub'], roles=current_identity.get('roles'))
                    ApplicationLogger.debug(f"Refreshed access token for identity [{current_identity['sub']}]")
                    
        except ExpiredSignatureError as e:
            ApplicationLogger.debug(f"Failed to refresh access token! Cookie is expired.")
        except CSRFError as e:
            ApplicationLogger.debug(f"Failed to refresh access token! No CSRF token in request.")
        except Exception as e:
            raise API_Error(
                f"Failed to refresh access token: {e}",
                stack_trace=traceback.format_exc()
            )

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
    def set_access_cookies(cls, response:Response, _id:str, roles:Optional[Union[str, list[str]]]='') -> Response:
        ''' Sets JWT access cookies in the response which will be stored by the client '''
        
        # HTTP Only cookies that store actual identity
        set_access_cookies(response, cls.create_access_token(_id, roles))
        set_refresh_cookies(response, cls.create_refresh_token(_id, roles))       

        return response

    @classmethod
    def set_identity_cookies(cls, response:Response, _id:str, username:Optional[str]=None, email:Optional[str]=None, roles:Optional[Union[str, list[str]]]='') -> Response:
        ''' Sets a JWT identity cookies in the response which will be stored by the client '''
        
        # Set access cookies
        cls.set_access_cookies(response, _id, roles)

        # JS accessible cookie that can be used to track the username and ID of the authed user by the client
        base_identity = [f"_id={_id}"]
        if username:
            base_identity.append(f"username={username}")
        if email:
            base_identity.append(f"email={email}")
        
        base_identity.append(f"roles={','.join(roles) if isinstance(roles, list) else roles}")

        response.set_cookie(
            cls.APP_IDENTITY_COOKIE,
            "|".join(base_identity),
            samesite='strict',
            max_age=App_Settings().jwt.access_token_expiration_secs
        )

        return response


    @classmethod
    def unset_identity_cookies(cls, response:Response) -> Response:
        ''' Unsets the JWT identity cookie in the response which will be purged by the client '''
        
        unset_jwt_cookies(response)
        response.set_cookie(cls.APP_IDENTITY_COOKIE, '', samesite='strict', expires=0)

        return response