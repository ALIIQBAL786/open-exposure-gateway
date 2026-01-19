from flask import jsonify
from pydantic import ValidationError #Field
from edge_cloud_management_api.managers.log_manager import logger
from edge_cloud_management_api.services.edge_cloud_services import PiEdgeAPIClientFactory

def create_qod_session(body: dict):
    """
    Creates a new QoD session
    """
    try:
        # Validate the input data using Pydantic
        # validated_data = AppManifest(**body)
        # validated_data_dict = validated_data.model_dump(mode="json")
        # validated_data_dict["_id"] = str(uuid.uuid4())
        pi_edge_factory = PiEdgeAPIClientFactory()
        api_client = pi_edge_factory.create_pi_edge_api_client()
        response = api_client.create_qod_session(body)
        return response

    except ValidationError as e:
        return jsonify({"error": "Invalid input", "details": e.errors()}), 400

    except Exception as e:
        return (
            jsonify({"error": "An unexpected error occurred", "details": str(e)}),
            500,
        )
    
def delete_qod_session(sessionId: str):
    """
    Creates a new QoD session
    """
    try:
        # Validate the input data using Pydantic
        # validated_data = AppManifest(**body)
        # validated_data_dict = validated_data.model_dump(mode="json")
        # validated_data_dict["_id"] = str(uuid.uuid4())
        pi_edge_factory = PiEdgeAPIClientFactory()
        api_client = pi_edge_factory.create_pi_edge_api_client()
        response = api_client.delete_qod_session(sessionId=sessionId)

        return response

    except ValidationError as e:
        return jsonify({"error": "Invalid input", "details": e.errors()}), 400

    except Exception as e:
        return (
            jsonify({"error": "An unexpected error occurred", "details": str(e)}),
            500,
        )
def get_qod_session(sessionId: str):
    """
    Creates a new QoD session
    """
    try:
        # Validate the input data using Pydantic
        # validated_data = AppManifest(**body)
        # validated_data_dict = validated_data.model_dump(mode="json")
        # validated_data_dict["_id"] = str(uuid.uuid4())
        pi_edge_factory = PiEdgeAPIClientFactory()
        api_client = pi_edge_factory.create_pi_edge_api_client()
        response = api_client.get_qod_session(sessionId=sessionId)
        # Insert into MongoDB
        # with MongoManager() as db:
        #     document_id = db.insert_document("apps", validated_data_dict)
        #     return (
        #         jsonify({"appId": str(document_id)}),
        #         201,
        #     )
        return response

    except ValidationError as e:
        return jsonify({"error": "Invalid input", "details": e.errors()}), 400

    except Exception as e:
        return (
            jsonify({"error": "An unexpected error occurred", "details": str(e)}),
            500,
        )
    
def create_traffic_influence_resource(body: dict):
        try:
            pi_edge_factory = PiEdgeAPIClientFactory()
            api_client = pi_edge_factory.create_pi_edge_api_client()
            response = api_client.create_traffic_influence_resource(body)
            return response
        except ValidationError as e:
            return jsonify({"error": "Invalid input", "details": e.errors()}), 400

        except Exception as e:
            return (
            jsonify({"error": "An unexpected error occurred", "details": str(e)}),
            500,
        )

def get_traffic_influence_resource(id: str):
    try:
            pi_edge_factory = PiEdgeAPIClientFactory()
            api_client = pi_edge_factory.create_pi_edge_api_client()
            response = api_client.get_traffic_influence_resource(id)
            return response
    except ValidationError as e:
            return jsonify({"error": "Invalid input", "details": e.errors()}), 400

    except Exception as e:
            return (
            jsonify({"error": "An unexpected error occurred", "details": str(e)}),
            500,
    )


def delete_traffic_influence_resource(id: str):
    try:
            pi_edge_factory = PiEdgeAPIClientFactory()
            api_client = pi_edge_factory.create_pi_edge_api_client()
            response = api_client.delete_traffic_influence_resource(id)
            return response
    except ValidationError as e:
            return jsonify({"error": "Invalid input", "details": e.errors()}), 400

    except Exception as e:
            return (
            jsonify({"error": "An unexpected error occurred", "details": str(e)}),
            500,
    )    

def get_all_traffic_influence_resources():
    try:
            pi_edge_factory = PiEdgeAPIClientFactory()
            api_client = pi_edge_factory.create_pi_edge_api_client()
            response = api_client.get_all_traffic_influence_resources()
            return response
    except ValidationError as e:
            return jsonify({"error": "Invalid input", "details": e.errors()}), 400

    except Exception as e:
            return (
            jsonify({"error": "An unexpected error occurred", "details": str(e)}),
            500,
    )
