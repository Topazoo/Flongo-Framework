    
from typing import Optional
from src.config.settings.app_settings.mongodb_settings import MongoDB_Settings
from pymongo import MongoClient

class Mongo_Collection:
    ''' MongoDB Collection client '''

    def __init__(self, collection:str, settings:MongoDB_Settings, database:Optional[str]=None):
        self.settings = settings
        self.database = database or settings.default_database
        self.collection = collection

        self.mongodb_client = self._get_mongodb_client()


    def _get_mongodb_client(self) -> MongoClient:
        ''' Get the MongoDB connection string '''

        return MongoClient(self.connection_string, connectTimeoutMS=self.settings.connection_timeout)


    def can_connect_to_mongo_db(self):
        ''' Tests if the connection to MongoDB is working '''

        return True if self.mongodb_client.server_info() else False
    

    @property
    def connection_string(self) -> str:
        # If it looks like an Atlas hostname (contains ".mongodb.net"), use the mongodb+srv:// scheme
        if self.settings.host and ".mongodb.net" in self.settings.host:
            return f"mongodb+srv://{self.settings.username}:{self.settings.password}@{self.settings.host}/{self.database}?retryWrites=true&w=majority"
        
        # Otherwise connect locally
        connection_uri = "mongodb://"
        if self.settings.username:
            connection_uri += f"{self.settings.username}:{self.settings.password}@"
        
        connection_uri += f"{self.settings.host}:{self.settings.port}/{self.database}"

        return connection_uri
