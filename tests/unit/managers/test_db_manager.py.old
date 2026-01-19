import pytest
from unittest.mock import patch
import mongomock

from edge_cloud_management_api.managers.db_manager import MongoManager


class TestConfig:
    MONGO_URI = "mongodb://test_admin:test_password@localhost:27017/test_db"


@pytest.fixture
def mock_mongo_manager():
    """
    Fixture to provide a MongoManager instance with a mocked MongoDB client.
    """

    with patch("edge_cloud_management_api.managers.db_manager.config", new=TestConfig):
        with patch(
            "edge_cloud_management_api.managers.db_manager.MongoClient",
            new=mongomock.MongoClient,
        ):
            # mongo_manager = MongoManager()
            # yield mongo_manager
            # mongo_manager.close_connection()
            with MongoManager() as mongo_manager:
                yield mongo_manager


@pytest.mark.unit
class TestMongoManager:
    """
    Test the MongoManager class.
    """

    # def test_insert_document(mock_mongo_manager):
    #     """
    #     Test the insert_document method.
    #     """
    #     inserted_id = mock_mongo_manager.insert_document(
    #         "test_collection", {"name": "Test User", "email": "
    def test_insert_document(self, mock_mongo_manager):
        """
        Test the insert_document method.
        """
        inserted_id = mock_mongo_manager.insert_document("test_collection", {"name": "Test User", "email": "test@example.com"})
        assert inserted_id is not None
        result = mock_mongo_manager.find_document("test_collection", {"_id": inserted_id})
        assert result["name"] == "Test User"

    def test_find_document(self, mock_mongo_manager):
        """
        Test the find_document method.
        """
        mock_mongo_manager.insert_document("test_collection", {"name": "Test User", "email": "test@example.com"})
        result = mock_mongo_manager.find_document("test_collection", {"name": "Test User"})
        assert result is not None
        assert result["email"] == "test@example.com"

    def test_find_documents(self, mock_mongo_manager):
        """
        Test the find_documents method.
        """
        mock_mongo_manager.insert_document("test_collection", {"name": "User 1", "email": "user1@example.com"})
        mock_mongo_manager.insert_document("test_collection", {"name": "User 2", "email": "user2@example.com"})
        results = mock_mongo_manager.find_documents("test_collection", {})
        assert len(list(results)) == 2

    def test_update_document(self, mock_mongo_manager):
        """
        Test the update_document method.
        """
        inserted_id = mock_mongo_manager.insert_document("test_collection", {"name": "User", "email": "user@example.com"})
        update_count = mock_mongo_manager.update_document("test_collection", {"_id": inserted_id}, {"name": "Updated User"})
        assert update_count == 1
        result = mock_mongo_manager.find_document("test_collection", {"_id": inserted_id})
        assert result["name"] == "Updated User"

    def test_delete_document(self, mock_mongo_manager):
        """
        Test the delete_document method.
        """
        inserted_id = mock_mongo_manager.insert_document("test_collection", {"name": "User", "email": "user@example.com"})
        delete_count = mock_mongo_manager.delete_document("test_collection", {"_id": inserted_id})
        assert delete_count == 1
        result = mock_mongo_manager.find_document("test_collection", {"_id": inserted_id})
        assert result is None

    def test_update_nonexistent_document(self, mock_mongo_manager):
        """
        Test updating a nonexistent document.
        """
        update_count = mock_mongo_manager.update_document("test_collection", {"name": "Nonexistent"}, {"name": "Updated"})
        assert update_count == 0

    def test_delete_nonexistent_document(self, mock_mongo_manager):
        """
        Test deleting a nonexistent document.
        """
        delete_count = mock_mongo_manager.delete_document("test_collection", {"name": "Nonexistent"})
        assert delete_count == 0
