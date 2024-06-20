import unittest
from unittest.mock import MagicMock
from mongod_db import MongoDBHandler

class MongoDBHandlerTests(unittest.TestCase):
    def setUp(self):
        self.handler = MongoDBHandler(collection_name='search-arena-test')

    def tearDown(self):
        self.handler.collection.delete_many({})

    def test_add_document(self):
        document = {"name": "John Doe", "age": 30}
        self.handler.add(document)
        result = self.handler.collection.find_one(document)
        self.assertIsNotNone(result)
        self.assertEqual(result["name"], "John Doe")
        self.assertEqual(result["age"], 30)

    def test_query_documents(self):
        document1 = {"name": "John Doe", "age": 30}
        document2 = {"name": "Jane Smith", "age": 25}
        self.handler.add(document1)
        self.handler.add(document2)
        query = {"age": {"$gt": 28}}
        results = self.handler.query(query)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "John Doe")
        self.assertEqual(results[0]["age"], 30)

if __name__ == "__main__":
    unittest.main()