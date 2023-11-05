from typing import Callable, Optional
from flask import Response
from ....api.requests.request import App_Request
from ....api.responses.api_json_response import API_JSON_Response
from ....api.responses.api_message_response import API_Message_Response
from ....config.enums.http_methods import HTTP_METHODS

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

    def GET(self, request:App_Request):
        ''' Gets a record from the MongoDB collection specified 
            using the payload from the request
        '''

        request.ensure_collection()
        request.normalize_id(enforce=False)

        if result:=list(request.run_mongo_operation() or []):
            return API_JSON_Response(result) if len(result) > 1 else API_JSON_Response(result[0])
        else:
            return API_JSON_Response(result, 404)
        

    def POST(self, request:App_Request):
        ''' Creates a record from the MongoDB collection specified 
            using the payload from the request
        '''

        request.ensure_collection()
        request.normalize_id(enforce=False)

        if _id:=request.run_mongo_operation(op='insert_one').inserted_id:
            return API_JSON_Response({"_id": str(_id)}, 201) 
        else:
            return API_Message_Response("Failed to create record in MongoDB", 500)
        

    def PUT(self, request:App_Request):
        ''' Updates a record from the MongoDB collection specified by ID
            using the payload from the request. Creates it if it does not exist
        '''

        request.ensure_collection()
        request.normalize_id()
        result = request.run_mongo_operation(
            op='update_many', 
            search_payload={"_id": request.payload.pop("_id")}, 
            set_payload=True, 
            upsert=True
        )

        if result:
            if upserted_id:=result.upserted_id:
                return API_JSON_Response({"_id": str(upserted_id)}, 201)
            if result.matched_count:
                return API_JSON_Response({}, 200)
            else:
                return API_JSON_Response({}, 404)
        else:
            return API_Message_Response("Failed to create record in MongoDB", 500)
        

    def PATCH(self, request:App_Request):
        ''' Updates a record from the MongoDB collection specified by ID
            using the payload from the request. Does not create it if it does not exist
        '''

        request.ensure_collection()
        request.normalize_id()
        result = request.run_mongo_operation(
            op='update_many',
            search_payload={"_id": request.payload.pop("_id")},
            set_payload=True
        )

        if result:
            return API_JSON_Response({}, 200) if result.matched_count else API_JSON_Response({}, 404)
        else:
            return API_Message_Response("Failed to create record in MongoDB", 500)


    def DELETE(self, request:App_Request):
        ''' Deletes a record from the MongoDB collection specified 
            using the payload from the request
        '''

        request.ensure_collection()
        request.normalize_id(enforce=False)
        
        if request.run_mongo_operation(op='delete_many').deleted_count:
            return API_JSON_Response({})
        else:
            return API_JSON_Response({}, 404)
        

    # Holds a reference of all methods for this route
    def __init__(self, **methods:Optional[Callable[[App_Request], Response]]):
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
