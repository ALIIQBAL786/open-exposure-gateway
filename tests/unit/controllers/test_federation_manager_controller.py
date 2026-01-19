import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from edge_cloud_management_api.controllers import federation_manager_controller


@pytest.fixture
def test_app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    with app.app_context():
        yield app


@pytest.mark.component
@patch("edge_cloud_management_api.controllers.federation_manager_controller.FederationManagerClientFactory")
def test_create_federation(mock_factory_class, test_app: Flask):
    """Test create_federation returns federation data"""
    body = {
        "origOPFederationId": "orig-123",
        "initialDate": "2024-01-01T00:00:00Z",
        "partnerStatusLink": "https://callback.example.com/status"
    }

    mock_client = MagicMock()
    mock_client.post_partner.return_value = {"federationContextId": "abc", "partnerOPFederationId": "partner-xyz"}
    mock_factory_class.return_value.create_federation_client.return_value = mock_client

    with test_app.test_request_context(json=body):
        response, status = federation_manager_controller.create_federation()

    assert status == 200
    data = response.get_json()
    assert "federationContextId" in data
    assert data["federationContextId"] == "abc"


@pytest.mark.component
@patch("edge_cloud_management_api.controllers.federation_manager_controller.FederationManagerClientFactory")
def test_get_federation(mock_factory_class, test_app: Flask):
    federation_context_id = "abc"

    mock_client = MagicMock()
    mock_client.get_partner.return_value = {"some": "data"}
    mock_factory_class.return_value.create_federation_client.return_value = mock_client

    with test_app.test_request_context():
        response, status = federation_manager_controller.get_federation(federation_context_id)

    assert status == 200
    assert response.get_json() == {"some": "data"}


@pytest.mark.component
@patch("edge_cloud_management_api.controllers.federation_manager_controller.FederationManagerClientFactory")
def test_delete_federation(mock_factory_class, test_app: Flask):
    federation_context_id = "abc"

    mock_client = MagicMock()
    mock_client.delete_partner.return_value = {"result": "Deleted"}
    mock_factory_class.return_value.create_federation_client.return_value = mock_client

    with test_app.test_request_context():
        response, status = federation_manager_controller.delete_federation(federation_context_id)

    assert status == 200
    assert response.get_json() == {"result": "Deleted"}


@pytest.mark.component
@patch("edge_cloud_management_api.controllers.federation_manager_controller.FederationManagerClientFactory")
def test_get_federation_context_ids(mock_factory_class, test_app: Flask):
    mock_client = MagicMock()
    mock_client.get_federation_context_ids.return_value = {"FederationContextId": "ctx-123"}
    mock_factory_class.return_value.create_federation_client.return_value = mock_client

    with test_app.test_request_context():
        response, status = federation_manager_controller.get_federation_context_ids()

    assert status == 200
    assert response.get_json() == {"FederationContextId": "ctx-123"}
