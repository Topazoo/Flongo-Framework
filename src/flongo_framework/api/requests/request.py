import traceback
from typing import Any, Optional
from bson import ObjectId
from pymongo.collection import Collection
from flask import Request

from .identity import Request_Identity
from ...api.responses.errors.api_error import API_Error

class App_Request:
    ''' Base class that wraps Flask's request and allows
        some additional data like the passed data, identity
        and MongoDB collection to be injected
    '''

    def __init__(self, 
            raw_request:Request,
            identity:Optional[Request_Identity]=None,
            payload:Optional[dict]=None,
            collection:Optional[Collection]=None
        ) -> None:
        # Raw Flask request
        self.raw_request = raw_request
        # JWT Identity parsed from cookies if available
        self.identity = identity
        # Data parsed from query string and request body if available
        self.payload = payload or {}
        # MongoDB collection instance to configured collection if available
        self.collection = collection


    def set_identity(self, identity:Request_Identity):
        self.identity = identity


    def set_payload(self, payload:dict):
        self.payload = payload


    def set_collection(self, collection:Collection):
        self.collection = collection


    def run_mongo_operation(self, op:str='find', search_payload:Optional[dict]=None, set_payload:bool=False, upsert:bool=False) -> Any:
        ''' Runs the specified operation on the stored MongoDB collection with a passed
            or with the stored payload 
        '''

        if self.collection != None:
            func = getattr(self.collection, op)
            if not search_payload:
                search_payload = self.payload

            if set_payload:
                if upsert:
                    return func(search_payload, {"$set": self.payload}, upsert=upsert)
                else:
                    return func(search_payload, {"$set": self.payload})
            else:
                return func(search_payload)


    def ensure_collection(self):
        ''' Ensure a MongoDB collection is specified for this Request or throw an exception '''

        if self.collection == None:
            raise API_Error(
                "No MongoDB collection was specified for this route",
                {'url': self.raw_request.root_url},
                stack_trace=traceback.format_exc()
            )
        

    def ensure_field(self, field:str, required_value:str='') -> Any:
        ''' Ensure a field is specified in this request payload and return the field value '''

        value = None
        if self.payload and not (value:=self.payload.get(field)):
            raise API_Error(
                f"Required field [{field}] not passed in request",
                {'url': self.raw_request.root_url, 'method': self.raw_request.method},
                stack_trace=traceback.format_exc()
            )
        
        if required_value and value != required_value:
            raise API_Error(
                f"Required field [{field}] passed in request did not have the required value",
                {
                    'url': self.raw_request.root_url, 
                    'method': self.raw_request.method,
                    'value': value,
                    'required_value': required_value
                },
                stack_trace=traceback.format_exc()
            )
        
        return value
    

    def normalize_id(self, field:str="_id", enforce:bool=True):
        ''' Convert a field from string to ObjectId '''

        if enforce:
            self.ensure_field(field)

        if field in self.payload:
            if ObjectId.is_valid(self.payload[field]):
                self.payload[field] = ObjectId(self.payload[field])
