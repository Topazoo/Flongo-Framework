# Typing
import traceback
from typing import Optional
from bson import ObjectId

from src.database.errors.database_error import DatabaseError

class Fixtures:
    ''' Class to facilitate applying database fixtures '''

    def __init__(self, fixtures:dict[str, list[dict]]) -> None:
        self.fixtures = self._validate_fixtures(fixtures)
        
    def _validate_fixtures(self, fixtures:dict[str, list]) -> dict[str, list]:
        ''' Validate fixture structure and return fixtures'''

        if fixtures and not isinstance(fixtures, dict):
            raise DatabaseError(
                f'Error in fixture definitions. The fixture definition must be a dictionary',
                stack_trace=traceback.format_exc()
            )

        if fixtures:
            for collection, items in fixtures.items():
                if not isinstance(items, list):
                    raise DatabaseError(
                        f'Error in fixture definitions for collection [{collection}]. The defined fixtures must be a list of dictionaries to insert in the database. Found a {type(items)}',
                        stack_trace=traceback.format_exc()
                    )

                for item in items:
                    if not isinstance(item, dict):
                        raise DatabaseError(
                            f'Error in fixture definitions for collection [{collection}]. The fixture definition must be a list of dictionaries, the list contained type {type(item)}',
                            stack_trace=traceback.format_exc()
                        )
                    if not item.get('_id'):
                        raise DatabaseError(
                            f'Error in fixture definitions for collection [{collection}]. The fixture definition:\n{item}\n is missing a MongoDB ObjectId in the _id field',
                            stack_trace=traceback.format_exc()
                        )
                    if not ObjectId.is_valid(item.get('_id')):
                     raise DatabaseError(
                            f'Error in fixture definitions for collection [{collection}]. The fixture definition:\n{item}\n has an invalid MongoDB ObjectId in the _id field',
                            stack_trace=traceback.format_exc()
                        )
            
            return fixtures
        
        return {}


    def get_fixtures(self) -> dict[str, list[dict]]:
        return self.fixtures