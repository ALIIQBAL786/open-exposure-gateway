import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from edge_cloud_management_api.controllers import app_controllers


@pytest.fixture
def test_app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    with app.app_context():
        yield app


@pytest.mark.component
@patch("edge_cloud_management_api.controllers.app_controllers.PiEdgeAPIClientFactory")
def test_delete_app(mock_factory_class, test_app: Flask):
    """Test delete_app returns dict"""
    app_id = "mock-app-id"
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.json.return_value = {"result": "deleted"}
    mock_response.status_code = 200
    mock_client.delete_app.return_value = mock_response

    mock_factory_class.return_value.create_pi_edge_api_client.return_value = mock_client

    with test_app.test_request_context():
        result = app_controllers.delete_app(app_id)

    assert isinstance(result, dict)
    assert result == {"result": "deleted"}


@pytest.mark.component
@patch("edge_cloud_management_api.controllers.app_controllers.PiEdgeAPIClientFactory")
def test_create_app_instance(mock_factory_class, test_app: Flask):
    """Test create_app_instance returns accepted response"""
    body = {
        "appId": "mock-app-id",
        "edgeCloudZoneId": "zone-1",
        "kubernetesClusterRef": "cluster-1"
    }

    mock_client = MagicMock()
    mock_client.deploy_service_function.return_value = {"deploymentId": "xyz-123"}
    mock_factory_class.return_value.create_pi_edge_api_client.return_value = mock_client

    with test_app.test_request_context(json=body):
        response, status_code = app_controllers.create_app_instance()

    assert status_code == 202
    data = response.get_json()
    assert "Application mock-app-id instantiation accepted" in data["message"]


@pytest.mark.component
@patch("edge_cloud_management_api.controllers.app_controllers.PiEdgeAPIClientFactory")
def test_get_app_instance(mock_factory_class, test_app: Flask):
    """Test get_app_instance returns app instances"""
    mock_client = MagicMock()
    mock_client.get_app_instances.return_value = [{"appInstanceId": "abc123"}]
    mock_factory_class.return_value.create_pi_edge_api_client.return_value = mock_client

    with test_app.test_request_context():
        response, status_code = app_controllers.get_app_instance()

    assert status_code == 200
    data = response.get_json()
    assert "appInstanceInfo" in data
    assert isinstance(data["appInstanceInfo"], list)
    assert data["appInstanceInfo"][0]["appInstanceId"] == "abc123"


@pytest.mark.component
@patch("edge_cloud_management_api.controllers.app_controllers.PiEdgeAPIClientFactory")
def test_delete_app_instance(mock_factory_class, test_app: Flask):
    """Test delete_app_instance returns dict"""
    app_instance_id = "instance-123"

    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.json.return_value = {"result": "Deleted"}
    mock_response.status_code = 200
    mock_client.delete_app_instance.return_value = mock_response

    mock_factory_class.return_value.create_pi_edge_api_client.return_value = mock_client

    with test_app.test_request_context():
        result = app_controllers.delete_app_instance(app_instance_id)

    assert isinstance(result, dict)
    assert result == {"result": "Deleted"}

