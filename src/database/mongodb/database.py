    
from typing import Optional
from src.config.settings.app_settings.mongodb_settings import MongoDB_Settings
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

from src.database.errors.database_error import DatabaseError

class MongoDB_Database:
    ''' MongoDB database client 
    
        Can be instantiated with a collection name, database name and database settings.
        ```
        settings = MongoDB_Settings()
        MongoDB_Database("collection", "db", settings)
        ```
        Collections can also be referenced using the [] operator:
        ```
        MongoDB_Database("db", settings)['collection]
        ```
        Collections can also be accessed using the "with" operator:
        ```
        with MongoDB_Database("collection", "db", settings) as db:
            pass
        ```
    '''

    def __init__(self, collection_name:Optional[str]=None, database_name:Optional[str]=None, settings:Optional[MongoDB_Settings]=None):
        self.settings = settings or MongoDB_Settings()
        self.database_name = database_name or self.settings.default_database
        self.collection_name = collection_name or ''

        self._client = self._get_client()
        

    def _get_client(self) -> MongoClient:
        ''' Get the MongoDB connection string '''

        return MongoClient(self.connection_string, connectTimeoutMS=self.settings.connection_timeout)


    @property
    def database(self) -> Database:
        ''' Get the MongoDB Database specified by this instance '''

        return self._client.get_database(self.database_name)


    @property
    def collection(self) -> Collection:
        ''' Get the MongoDB Collection specified by this instance '''

        return self._get_collection(self.collection_name)


    @property
    def connection_string(self) -> str:
        ''' Get the MongoDB connection string '''
        
        # If it looks like an Atlas hostname (contains ".mongodb.net"), use the mongodb+srv:// scheme
        if self.settings.host and ".mongodb.net" in self.settings.host:
            return f"mongodb+srv://{self.settings.username}:{self.settings.password}@{self.settings.host}/{self.database_name}?retryWrites=true&w=majority"
        
        # Otherwise connect locally
        connection_uri = "mongodb://"
        if self.settings.username:
            connection_uri += f"{self.settings.username}:{self.settings.password}@"
        
        connection_uri += f"{self.settings.host}:{self.settings.port}/{self.database_name}"

        return connection_uri


    def is_valid_connection(self):
        ''' Tests if the connection to MongoDB is working '''

        return True if self._client.server_info() else False
    

    def _get_collection(self, collection_name:str):
        ''' Get a MongoDB collection by name '''
        if not collection_name:
            raise DatabaseError(f"Can't access a collection without a collection_name!")
    
        return self.database.get_collection(collection_name)
    

    def __getitem__(self, collection_name: str) -> Collection:
        ''' Get a MongoDB Collection by name with []'''

        return self._get_collection(collection_name)
    

    def __enter__(self):
        ''' Enter the context and return the default collection '''

        return self.collection


    def __exit__(self, exc_type, exc_val, exc_tb):
        ''' Exit the context and handle cleanup '''

        self._client.close()
