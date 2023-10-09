    
import logging
from typing import Optional
from src.config.settings.app_settings.mongodb_settings import MongoDB_Settings
from pymongo import TEXT, MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.errors import OperationFailure

from src.database.errors.database_error import DatabaseError
from src.database.mongodb.index.base import Index
from src.database.mongodb.index.indices import Indices

import traceback

from src.utils.logging.loggers.database import DatabaseLogger

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
        # TODO - Indices docs
    '''

    def __init__(self, 
            collection_name:Optional[str]=None, 
            database_name:Optional[str]=None, 
            settings:Optional[MongoDB_Settings]=None,
            indices:Optional[Indices]=None,
            connection_must_be_valid:bool=True
        ):
        self.settings = settings or MongoDB_Settings()
        self.indices = indices or Indices([])
        self.database_name = database_name or self.settings.default_database
        self.collection_name = collection_name or ''

        self._configure_logger()
        self._client = self._get_client()

        if connection_must_be_valid:
            self.validate_connection(True)
        

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
    

    def _get_collection(self, collection_name:str):
        ''' Get a MongoDB collection by name '''
        if not collection_name:
            raise DatabaseError(f"Can't access a collection without a collection_name!")
    
        return self.database.get_collection(collection_name)
    
    
    def _configure_logger(self):
        int_log_level =  DatabaseLogger.log_level_int(self.settings.log_level or '')

        # Database
        logging.basicConfig(level=int_log_level)
        logging.getLogger(DatabaseLogger.LOGGER_NAME).setLevel(int_log_level)


    def __getitem__(self, collection_name: str) -> Collection:
        ''' Get a MongoDB Collection by name with []'''

        return self._get_collection(collection_name)
    

    def __enter__(self):
        ''' Enter the context and return the default collection '''

        return self.collection


    def __exit__(self, exc_type, exc_val, exc_tb):
        ''' Exit the context and handle cleanup '''

        self._client.close()


    def validate_connection(self, raise_exception:bool=False) -> bool:
        ''' Tests if the connection to MongoDB is working '''

        result = True if self._client.server_info() else False
        if not result and raise_exception:
            raise DatabaseError(
                f"MongoDB_Database: Could not connect to the database!",
                data={
                    'host': self.settings.host,
                    'port': self.settings.port,
                    'username': self.settings.username,
                    'password': '<SET>' if self.settings.password else '<NOT SET>'
                }
            )
        
        if result:
            DatabaseLogger.debug(f"Connected to MongoDB on [{self.connection_string}]!")
        
        return result
    

    def add_index(self, index:Index, create:bool=True, background:bool=False):
        ''' Add an index and create it by default '''
        
        self.indices.add_index(index)
        if create:
            self.create_index(index, background)


    def create_index(self, index:Index, background:bool=False):
        ''' Create a database index '''
        
        try:
            index_collection = self._get_collection(index.collection_name)
            # Create a text index
            if index.is_text:
                index_collection.create_index([
                    (index.field_name, TEXT)
                ], background=background)
            
            # Create a compound index
            elif index.compound_index:
                index_collection.create_index([
                    (index.field_name, index.order), 
                    (index.compound_index.field_name, index.compound_index.order)
                ], **index.properties, background=background)

            # Create a standard index
            else:
                index_collection.create_index([
                    (index.field_name, index.order),
                ], **index.properties, background=background)

            DatabaseLogger.info(f"Created {index.index_type} index on field [{index.field_name}] for collection [{index.collection_name}]")

        except OperationFailure as e:
            if e.code == 85:
                DatabaseLogger.warn(f"{index.index_type.capitalize()} Index for field [{index.field_name}] in collection [{index.collection_name}] already exists!")
            else:
                raise DatabaseError(
                    f"MongoDB_Database: Index creation failed!",
                    e.code,
                    {
                        "collection_name": index.collection_name, 
                        "field": index.field_name,
                        "index_type": index.index_type,
                        "details": e.details
                    }
                )
        
        except Exception as e:
            raise DatabaseError(
                    f"MongoDB_Database: Error creating index!",
                    data={
                        "collection_name": index.collection_name, 
                        "field": index.field_name,
                        "index_type": index.index_type
                    },
                    stack_trace=traceback.format_exc()
                )
        

    def create_indices(self, background:bool=False):
        ''' Creates all stored indices on the connected database '''

        # Ensure a connection can be made
        self.validate_connection(raise_exception=True)

        # Create all indices
        for index in self.indices:
            self.create_index(index, background)
