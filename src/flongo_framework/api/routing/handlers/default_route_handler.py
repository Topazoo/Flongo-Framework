from ....api.responses.api_json_response import API_JSON_Response
from ....api.responses.api_message_response import API_Message_Response
from ....config.enums.http_methods import HTTP_METHODS

from flask import Request
from pymongo.collection import Collection
from ....api.routing.types import HandlerMethod
from ....api.routing.handlers.route_handler import Route_Handler


class Default_Route_Handler(Route_Handler):
    ''' Class that allows functions to be bound to specific HTTP 
        methods like GET or POST but uses a default operation 
        if a custom function isn't passed.

        - GET: Gets a record from the MongoDB collection specified using the payload from the request
        - POST: Creates a record from the MongoDB collection specified using the payload from the request
        - PUT: Updates a record from the MongoDB collection specified by ID using the payload from the request. Creates it if it does not exist
        - PATCH: Updates a record from the MongoDB collection specified by ID using the payload from the request. Does not create it if it does not exist
        - DELETE: Deletes a record from the MongoDB collection specified using the payload from the request
    '''

    def GET(self, request:Request, payload:dict, collection:Collection):
        ''' Gets a record from the MongoDB collection specified 
            using the payload from the request
        '''

        self.ensure_collection(request.root_url, collection)
        self.normalize_id(payload)

        if result:=list(collection.find(payload)):
            return API_JSON_Response(result) if len(result) > 1 else API_JSON_Response(result[0])
        else:
            return API_JSON_Response(result, 404)
        

    def POST(self, request:Request, payload:dict, collection:Collection):
        ''' Creates a record from the MongoDB collection specified 
            using the payload from the request
        '''

        self.ensure_collection(request.root_url, collection)
        self.normalize_id(payload)

        if _id:=collection.insert_one(payload).inserted_id:
            return API_JSON_Response({"_id": str(_id)}, 201) 
        else:
            return API_Message_Response("Failed to create record in MongoDB", 500)
        

    def PUT(self, request:Request, payload:dict, collection:Collection):
        ''' Updates a record from the MongoDB collection specified by ID
            using the payload from the request. Creates it if it does not exist
        '''

        self.ensure_collection(request.root_url, collection)
        self.ensure_field(request.root_url, request.method.upper(), "_id", payload)
        self.normalize_id(payload)

        result = collection.update_one({"_id": payload.pop("_id")}, {"$set": payload}, upsert=True)
        if result:
            if upserted_id:=result.upserted_id:
                return API_JSON_Response({"_id": str(upserted_id)}, 201)
            if result.matched_count:
                return API_JSON_Response({}, 200)
            else:
                return API_JSON_Response({}, 404)
        else:
            return API_Message_Response("Failed to create record in MongoDB", 500)
        

    def PATCH(self, request:Request, payload:dict, collection:Collection):
        ''' Updates a record from the MongoDB collection specified by ID
            using the payload from the request. Does not create it if it does not exist
        '''

        self.ensure_collection(request.root_url, collection)
        self.ensure_field(request.root_url, request.method.upper(), "_id", payload)
        self.normalize_id(payload)

        result = collection.update_one({"_id": payload.pop("_id")}, {"$set": payload})
        if result:
            return API_JSON_Response({}, 200) if result.matched_count else API_JSON_Response({}, 404)
        else:
            return API_Message_Response("Failed to create record in MongoDB", 500)


    def DELETE(self, request:Request, payload:dict, collection:Collection):
        ''' Deletes a record from the MongoDB collection specified 
            using the payload from the request
        '''

        self.ensure_collection(request.root_url, collection)
        self.normalize_id(payload)

        if collection.delete_one(payload).deleted_count:
            return API_JSON_Response({})
        else:
            return API_JSON_Response({}, 404)
        

    # Holds a reference of all methods for this route
    def __init__(self, **methods:HandlerMethod):
        self.methods = {
            "GET": self.GET,
            "POST": self.POST,
            "PUT": self.PUT, 
            "PATCH": self.PATCH,
            "DELETE": self.DELETE
        }

        for method, func in methods.items():
            normalized_method = method.upper()
            # Ensure the method is a valid HTTP method
            if normalized_method.lower() not in HTTP_METHODS:
                raise ValueError(f"Routehandler: [{normalized_method}] is not a valid HTTP method.")

            # Create a function on this handler tied
            # for a method like GET tied to a function
            # that should run when it is called 
            setattr(self, normalized_method, func)
            self.methods[normalized_method] = func
