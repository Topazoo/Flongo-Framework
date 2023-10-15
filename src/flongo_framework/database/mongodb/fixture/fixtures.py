import traceback

from ....database.errors.database_error import DatabaseError
from ....database.mongodb.fixture.base import MongoDB_Fixture

class MongoDB_Fixtures:
    ''' Class to facilitate applying database fixtures '''

    def __init__(self, *fixtures:MongoDB_Fixture) -> None:
        self._fixtures = self._validate_fixtures(list(fixtures))
        
    def _validate_fixtures(self, fixtures:list[MongoDB_Fixture]) -> list[MongoDB_Fixture]:
        ''' Validate fixture structure and return fixtures'''

        if fixtures and not isinstance(fixtures, list):
            raise DatabaseError(
                f'Error in fixture definitions. The fixture definition must be a list of MongoDB_Fixture objects',
                stack_trace=traceback.format_exc()
            )

        if fixtures:
            for fixture in fixtures:
                if not isinstance(fixture, MongoDB_Fixture):
                    raise DatabaseError(
                        f'Error in fixture definitions! The defined fixtures must be a list of MongoDB_Fixture objects to insert in the database. Found a {type(fixture)}',
                        stack_trace=traceback.format_exc()
                    )
            
            return fixtures
        
        return []


    def get_fixtures(self) -> list[MongoDB_Fixture]:
        return self._fixtures
    

    def __len__(self):
        return len(self._fixtures)
