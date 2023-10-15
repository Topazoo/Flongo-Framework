import traceback

from bson import ObjectId
from ....database.errors.database_error import DatabaseError


class MongoDB_Fixture:
    ''' Stores MongoDB fixture information '''

    def __init__(self, collection_name:str, data:dict):

        self.collection_name = collection_name
        self.data = self._validate_fixture_data(data)


    def _validate_fixture_data(self, data:dict) -> dict:
        ''' Validate the fixture is defined properly '''

        if data and not isinstance(data, dict):
            raise DatabaseError(
                f'Error in fixture definitions. The fixture definition must be a dictionary object',
                stack_trace=traceback.format_exc()
            )

        _id = data.get('_id')
        if not _id:
            raise DatabaseError(
                f'Error in fixture definitions for collection [{self.collection_name}]. The fixture definition:\n{data}\n is missing a MongoDB ObjectId in the _id field',
                stack_trace=traceback.format_exc()
            )
        
        if not ObjectId.is_valid(_id):
            raise DatabaseError(
                f'Error in fixture definitions for collection [{self.collection_name}]. The fixture definition:\n{data}\n has an invalid MongoDB ObjectId in the _id field',
                stack_trace=traceback.format_exc()
            )
        
        if not isinstance(_id, ObjectId):
            data['_id'] = ObjectId(_id)
        
        return data
