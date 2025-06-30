#!/usr/bin/env python
# coding: utf-8

from pymongo import MongoClient
from bson.objectid import ObjectId
import os
import logging

class MongoDBCRUD(object):
    """ 
    Generic CRUD operations for any MongoDB database and collection
    This class provides reusable database operations without hard-coded values
    """
    
    def __init__(self, username=None, password=None, host=None, port=None, 
                 database_name=None, collection_name=None, auth_source="admin"):
        """
        Initialize the MongoDB CRUD client with flexible parameters
        
        Args:
            username (str): MongoDB username (can be None for no auth)
            password (str): MongoDB password (can be None for no auth)
            host (str): MongoDB host address
            port (int): MongoDB port number
            database_name (str): Name of the database to connect to
            collection_name (str): Name of the collection to operate on
            auth_source (str): Authentication database (default: "admin")
        """
        
        # Set up logging
        self.logger = logging.getLogger(__name__)
        
        # Store connection parameters
        self.username = username or os.getenv('MONGO_USERNAME')
        self.password = password or os.getenv('MONGO_PASSWORD')
        self.host = host or os.getenv('MONGO_HOST', 'localhost')
        self.port = port or int(os.getenv('MONGO_PORT', 27017))
        self.database_name = database_name or os.getenv('MONGO_DATABASE')
        self.collection_name = collection_name or os.getenv('MONGO_COLLECTION')
        self.auth_source = auth_source
        
        # Validate required parameters
        if not self.database_name:
            raise ValueError("Database name is required")
        if not self.collection_name:
            raise ValueError("Collection name is required")
        
        # Initialize connections
        self._connect()
    
    def _connect(self):
        """Establish connection to MongoDB"""
        try:
            # Build connection string based on authentication requirements
            if self.username and self.password:
                connection_string = f'mongodb://{self.username}:{self.password}@{self.host}:{self.port}/?authSource={self.auth_source}'
            else:
                connection_string = f'mongodb://{self.host}:{self.port}'
            
            self.client = MongoClient(connection_string)
            self.database = self.client[self.database_name]
            self.collection = self.database[self.collection_name]
            
            # Test the connection
            self.database.command('ping')
            self.logger.info(f"Successfully connected to MongoDB: {self.database_name}.{self.collection_name}")
            print(f"Connection to MongoDB successful: {self.database_name}.{self.collection_name}")
            
        except Exception as e:
            self.logger.error(f"Error connecting to MongoDB: {e}")
            print(f"Error connecting to MongoDB: {e}")
            raise e
    
    def switch_collection(self, new_collection_name):
        """
        Switch to a different collection in the same database
        
        Args:
            new_collection_name (str): Name of the new collection
        """
        self.collection_name = new_collection_name
        self.collection = self.database[new_collection_name]
        print(f"Switched to collection: {new_collection_name}")
    
    def switch_database(self, new_database_name, new_collection_name=None):
        """
        Switch to a different database and optionally a different collection
        
        Args:
            new_database_name (str): Name of the new database
            new_collection_name (str, optional): Name of the new collection
        """
        self.database_name = new_database_name
        self.database = self.client[new_database_name]
        
        if new_collection_name:
            self.collection_name = new_collection_name
            self.collection = self.database[new_collection_name]
        else:
            self.collection = self.database[self.collection_name]
        
        print(f"Switched to database: {new_database_name}.{self.collection_name}")
    
    def create(self, data):
        """
        Insert a document into the collection
        
        Args:
           data (dict): A dictionary containing key/value pairs for the document
           
        Returns:
           bool: True if successful insert, False otherwise
        """
        try:
            if data is not None and isinstance(data, dict):
                result = self.collection.insert_one(data)
                if result.inserted_id:
                    self.logger.info(f"Document inserted with ID: {result.inserted_id}")
                    return True
                else:
                    return False
            else:
                self.logger.warning("Invalid data provided for create operation")
                print("Error: Data parameter must be a non-empty dictionary")
                return False
        except Exception as e:
            self.logger.error(f"Error inserting document: {e}")
            print(f"Error inserting document: {e}")
            return False
    
    def read(self, query=None):
        """
        Query for documents from the collection
        
        Args: 
            query (dict, optional): A dictionary containing key/value lookup pairs.
                                  If None, returns all documents.
            
        Returns:
             list: A list of documents if successful, empty list otherwise
        """
        try:
            # Default to empty dict if no query provided (returns all documents)
            if query is None:
                query = {}
            
            if isinstance(query, dict):
                cursor = self.collection.find(query)
                result_list = list(cursor)
                self.logger.info(f"Found {len(result_list)} documents")
                return result_list
            else:
                self.logger.warning("Invalid query provided for read operation")
                print("Error: Query parameter must be a dictionary")
                return []
        except Exception as e:
            self.logger.error(f"Error querying documents: {e}")
            print(f"Error querying documents: {e}")
            return []
    
    def update(self, query, update_data, update_many=True):
        """
        Update document(s) in the collection
        
        Args:
            query (dict): A dictionary containing key/value pairs to find documents
            update_data (dict): A dictionary containing the update operations
            update_many (bool): If True, update all matching documents. If False, update only the first match.
            
        Returns:
            int: Number of documents modified, 0 if no documents were modified
        """
        try:
            if query is not None and isinstance(query, dict) and \
               update_data is not None and isinstance(update_data, dict):
                
                # Choose update method based on update_many parameter
                if update_many:
                    result = self.collection.update_many(query, {"$set": update_data})
                else:
                    result = self.collection.update_one(query, {"$set": update_data})
                
                self.logger.info(f"Updated {result.modified_count} documents")
                return result.modified_count
            else:
                self.logger.warning("Invalid parameters provided for update operation")
                print("Error: Both query and update_data parameters must be dictionaries")
                return 0
        except Exception as e:
            self.logger.error(f"Error updating documents: {e}")
            print(f"Error updating documents: {e}")
            return 0
    
    def delete(self, query, delete_many=True):
        """
        Delete document(s) from the collection
        
        Args:
            query (dict): A dictionary containing key/value pairs to find documents to delete
            delete_many (bool): If True, delete all matching documents. If False, delete only the first match.
            
        Returns:
            int: Number of documents deleted, 0 if no documents were deleted
        """
        try:
            if query is not None and isinstance(query, dict):
                # Choose delete method based on delete_many parameter
                if delete_many:
                    result = self.collection.delete_many(query)
                else:
                    result = self.collection.delete_one(query)
                
                self.logger.info(f"Deleted {result.deleted_count} documents")
                return result.deleted_count
            else:
                self.logger.warning("Invalid query provided for delete operation")
                print("Error: Query parameter must be a dictionary")
                return 0
        except Exception as e:
            self.logger.error(f"Error deleting documents: {e}")
            print(f"Error deleting documents: {e}")
            return 0
    
    def count_documents(self, query=None):
        """
        Count documents in the collection
        
        Args:
            query (dict, optional): Filter criteria. If None, counts all documents.
            
        Returns:
            int: Number of documents matching the query
        """
        try:
            if query is None:
                query = {}
            
            if isinstance(query, dict):
                count = self.collection.count_documents(query)
                return count
            else:
                print("Error: Query parameter must be a dictionary")
                return 0
        except Exception as e:
            self.logger.error(f"Error counting documents: {e}")
            print(f"Error counting documents: {e}")
            return 0
    
    def close_connection(self):
        """Close the MongoDB connection"""
        try:
            if self.client:
                self.client.close()
                self.logger.info("MongoDB connection closed")
                print("MongoDB connection closed successfully")
        except Exception as e:
            self.logger.error(f"Error closing connection: {e}")
            print(f"Error closing connection: {e}")
    
    def get_collection_info(self):
        """
        Get information about the current collection
        
        Returns:
            dict: Collection statistics and information
        """
        try:
            stats = self.database.command("collStats", self.collection_name)
            info = {
                "database": self.database_name,
                "collection": self.collection_name,
                "document_count": stats.get("count", 0),
                "size_bytes": stats.get("size", 0),
                "avg_document_size": stats.get("avgObjSize", 0)
            }
            return info
        except Exception as e:
            self.logger.error(f"Error getting collection info: {e}")
            return {}


# Convenience class for Animal Shelter specific operations
class AnimalShelter(MongoDBCRUD):
    """
    Animal Shelter specific CRUD operations
    Inherits from the generic MongoDBCRUD class
    """
    
    def __init__(self, username="aacuser", password="SNHU1234", 
                 host=None, port=None, database_name="AAC", collection_name="animals"):
        """
        Initialize Animal Shelter CRUD with default values for AAC database
        
        Args:
            username (str): MongoDB username (default: "aacuser")
            password (str): MongoDB password (default: "SNHU1234") 
            host (str): MongoDB host (default: from environment or localhost)
            port (int): MongoDB port (default: from environment or 27017)
            database_name (str): Database name (default: "AAC")
            collection_name (str): Collection name (default: "animals")
        """
        super().__init__(username, password, host, port, database_name, collection_name)
    
    def find_rescue_candidates(self, rescue_type="water"):
        """
        Find animals suitable for specific rescue training
        
        Args:
            rescue_type (str): Type of rescue training ("water", "mountain", "disaster")
            
        Returns:
            list: List of suitable animals
        """
        rescue_criteria = {
            "water": {
                "animal_type": "Dog",
                "breed": {"$in": ["Labrador Retriever Mix", "Chesapeake Bay Retriever", 
                                "Newfoundland", "Portuguese Water Dog"]},
                "$expr": {
                    "$and": [
                        {"$gte": ["$age_upon_outcome_in_weeks", 26]},
                        {"$lte": ["$age_upon_outcome_in_weeks", 156]}
                    ]
                }
            },
            "mountain": {
                "animal_type": "Dog", 
                "breed": {"$in": ["German Shepherd", "Alaskan Malamute", "Old English Sheepdog",
                                "Siberian Husky", "Rottweiler"]},
                "$expr": {
                    "$and": [
                        {"$gte": ["$age_upon_outcome_in_weeks", 26]},
                        {"$lte": ["$age_upon_outcome_in_weeks", 156]}
                    ]
                }
            },
            "disaster": {
                "animal_type": "Dog",
                "breed": {"$in": ["Doberman Pinscher", "German Shepherd", "Golden Retriever",
                                "Bloodhound", "Rottweiler"]},
                "$expr": {
                    "$and": [
                        {"$gte": ["$age_upon_outcome_in_weeks", 20]},
                        {"$lte": ["$age_upon_outcome_in_weeks", 300]}
                    ]
                }
            }
        }
        
        if rescue_type in rescue_criteria:
            return self.read(rescue_criteria[rescue_type])
        else:
            print(f"Unknown rescue type: {rescue_type}")
            return []