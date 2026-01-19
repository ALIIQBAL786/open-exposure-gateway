from pymongo import MongoClient
from edge_cloud_management_api.configs.env_config import config


class MongoManager:
    """
    A utility class for managing MongoDB operations.
    The class implements the context manager protocol to ensure that the connection is closed after use.

    Methods:
        insert_document: Inserts a document into a collection.
        find_document: Finds a single document in a collection.
        find_documents: Finds multiple documents in a collection.
        update_document: Updates a single document in a collection.
        delete_document: Deletes a single document in a collection.
        close_connection: Closes the MongoDB connection.

    Example:
        with MongoManager() as db:
            db.insert_document("users", {"name": "Test User", "email": "test-user@sunrise6g.eu"})

    """

    def __init__(self, mongo_uri=config.MONGO_URI):
        """
        Initializes the MongoDB connection using the URI from Config.
        """
        if not mongo_uri:
            raise ValueError("MONGO_URI is not set in the environment configuration.")

        self.client = MongoClient(mongo_uri, maxPoolSize=50)
        mongo_db_name: str = mongo_uri.split("/")[-1].split("?")[0]
        self.db = self.client[mongo_db_name]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()

    def insert_document(self, collection_name, document):
        """
        Inserts a document into the specified collection.
        """
        collection = self.db[collection_name]
        result = collection.insert_one(document)
        return result.inserted_id

    def find_document(self, collection_name, query):
        """
        Finds a single document based on the query.
        """
        collection = self.db[collection_name]
        return collection.find_one(query)

    def find_documents(self, collection_name, query):
        """
        Finds multiple documents based on the query.
        """
        collection = self.db[collection_name]
        return collection.find(query)

    def update_document(self, collection_name, query, update_data):
        """
        Updates a single document based on the query.
        """
        collection = self.db[collection_name]
        result = collection.update_one(query, {"$set": update_data})
        return result.modified_count

    def delete_document(self, collection_name, query):
        """
        Deletes a single document based on the query.
        """
        collection = self.db[collection_name]
        result = collection.delete_one(query)
        return result.deleted_count

    def close_connection(self):
        """
        Closes the MongoDB connection.
        """
        self.client.close()
