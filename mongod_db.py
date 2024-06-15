from typing import Any, Dict, List
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import os
from dotenv import load_dotenv


load_dotenv()


def mongo_db_uri():
    return os.getenv("MONGODB_URI")


class MongoDBHandler:
    def __init__(
        self,
        uri: str = mongo_db_uri(),
        db_name: str = "search-arena",
        collection_name: str = "search-arena-usage",
    ) -> None:
        """
        Initializes the MongoDBHandler with the specified database and collection.

        Args:
            uri (str): The MongoDB URI connection string.
            db_name (str): The name of the database.
            collection_name (str): The name of the collection.
        """
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def add(self, document: Dict[str, Any]) -> None:
        """
        Adds a document to the MongoDB collection.

        Args:
            document (Dict[str, Any]): The document to be added to the collection.

        Raises:
            PyMongoError: If an error occurs while inserting the document.
        """
        try:
            self.collection.insert_one(document)
        except PyMongoError as e:
            print(f"Error: {e}")
            raise

    def query(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Queries documents from the MongoDB collection based on the provided query.

        Args:
            query (Dict[str, Any]): The query to filter documents.

        Returns:
            List[Dict[str, Any]]: A list of documents that match the query.

        Raises:
            PyMongoError: If an error occurs while querying the documents.
        """
        try:
            return list(self.collection.find(query))
        except PyMongoError as e:
            print(f"Error: {e}")
            raise
