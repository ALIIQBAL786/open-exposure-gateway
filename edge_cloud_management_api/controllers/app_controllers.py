from flask import jsonify, request
from pydantic import ValidationError
from edge_cloud_management_api.managers.log_manager import logger
from edge_cloud_management_api.services.edge_cloud_services import PiEdgeAPIClientFactory
from edge_cloud_management_api.services.federation_services import FederationManagerClientFactory
from edge_cloud_management_api.services.storage_service import get_zone
from edge_cloud_management_api.services.storage_service import get_fed

factory = FederationManagerClientFactory()
federation_client = factory.create_federation_client()

class NotFound404Exception(Exception):
    pass


def submit_app(body: dict):
    """
    Controller for submitting application metadata.
    """
    try:
        pi_edge_factory = PiEdgeAPIClientFactory()
        api_client = pi_edge_factory.create_pi_edge_api_client()
        response = api_client.submit_app(body)
        return response

    except ValidationError as e:
        return jsonify({"error": "Invalid input", "details": e.errors()}), 400

    except Exception as e:
        return (
            jsonify({"error": "An unexpected error occurred", "details": str(e)}),
            500,
        )


def get_apps(x_correlator=None):
    """Retrieve metadata information of all applications"""
    try:
        pi_edge_factory = PiEdgeAPIClientFactory()
        api_client = pi_edge_factory.create_pi_edge_api_client()
        registered_apps = api_client.get_service_functions_catalogue()
        return registered_apps
    except Exception as e:
        return (
            jsonify({"error": "An unexpected error occurred", "details": str(e)}),
            500,
        )


def get_app(appId, x_correlator=None):
    """Retrieve the information of an Application"""
    try:
        pi_edge_factory = PiEdgeAPIClientFactory()
        api_client = pi_edge_factory.create_pi_edge_api_client()
        response = api_client.get_app(appId)
        return response

    except NotFound404Exception:
        return (
            jsonify({"status": 404, "code": "NOT_FOUND", "message": "Resource does not exist"}),
            404,
        )

    except Exception as e:
        return (
            jsonify({"error": "An unexpected error occurred", "details": str(e)}),
            500,
        )


def delete_app(appId, x_correlator=None):
    """Delete Application metadata from an Edge Cloud Provider"""
    try:
        pi_edge_factory = PiEdgeAPIClientFactory()
        api_client = pi_edge_factory.create_pi_edge_api_client()
        response = api_client.delete_app(appId=appId)
        return response

    except NotFound404Exception:
        return (
            jsonify({"status": 404, "code": "NOT_FOUND", "message": "Resource does not exist"}),
            404,
        )

    except Exception as e:
        return (
            jsonify({"status": 500, "code": "INTERNAL", "message": f"Internal server error: {str(e)}"}),
            500,
        )

def create_app_instance():
    logger.info("Received request to create app instance")
    try:
       body = request.get_json()
       logger.debug(f"Request body: {body}")
       
       app_id = body.get("appId")
       app_zones = body.get("appZones")
       pi_edge_client_factory = PiEdgeAPIClientFactory()
       pi_edge_client = pi_edge_client_factory.create_pi_edge_api_client()
       
       if not app_id or not app_zones :
           return jsonify({"error": "Missing required fields: appId, edgeCloudZoneId, or kubernetesCLusterRef"}), 400
       
       zone = get_zone(app_zones[0].get('EdgeCloudZone').get('edgeCloudZoneId'))
       if zone.get('isLocal')=='false':
           # Step 1: retrieve app metadata
           appData = pi_edge_client.get_app(appId=app_id).get('appManifest')
           #Step 2: compose GSMA artefact payload
           artefact = {}
           artefact['artefactId'] = app_id
           artefact['appProviderId'] = appData.get('appProvider')
           artefact['artefactName'] = appData.get('name')
           artefact['artefactVersionInfo'] = appData.get('version')
           artefact['artefactDescription'] = ''
           repoInfo = appData.get('appRepo')
           artefact['repoType'] = repoInfo.get('type')
           artefact['artefactRepoLocation'] = {'repoURL': repoInfo.get('imagePath'), 'userName': repoInfo.get('userName'), 'password': repoInfo.get('credentials'), 'token': ''}
           exposedInterfaces = []
           networkInterfaces = appData.get('componentSpec')[0].get('networkInterfaces')
           for ni in networkInterfaces:
               interface = {'interfaceId': '', 'commProtocol': ni.get('protocol'), 'commPort': ni.get('port'), 'visibilityType': ni.get('visibilityType'), 'network': '', 'InterfaceName': ''}
               exposedInterfaces.append(interface)
           artefact['componentSpec'] = [
               {
                   'componentName': appData.get('name'), 
                   'numOfInstances': 0, 
                   'restartPolicy': 'RESTART_POLICY_ALWAYS', 
                   'exposedInterfaces': exposedInterfaces, 
                   'compEnvParams': [],
                   'persistentVolumes': []
                }
            ]
           # Step 3: Send artefact to local fed manager
           fed_token = get_fed(zone.get('fedContextId')).get('token')
           create_artefact_response = federation_client.create_artefact(artefact=artefact, federation_context_id=zone.get('fedContextId'), token=fed_token)
           # Step 4: Onboard app
           if create_artefact_response.status_code == 200 or create_artefact_response.status_code ==409:
                # Step 5: Create GSM onboard app payload
                onboard_app = {}
                onboard_app['appId'] = app_id
                onboard_app['appProviderId'] = appData.get('appProvider')
                onboard_app['appDeploymentZones'] = []
                appMetaData = {}
                appMetaData['appName'] = appData.get('name')
                appMetaData['version'] = appData.get('version')
                onboard_app['appMetaData'] = appMetaData
                onboard_app['appComponentSpecs'] = [{'serviceNameNB': appData.get('name'),
                                                     'serviceNameEW': appData.get('name'),
                                                     'componentName': appData.get('name'),
                                                     'artefactId': app_id
                                                     }
                                                   ]
                # Step 6: Onboard app at partner
                onboard_app_response = federation_client.onboard_application(federation_context_id=zone.get('fedContextId'), body=onboard_app, token=fed_token)
                if onboard_app_response.status_code==200:
                    # Step 7: Construct GSMA deployment payload
                    deploy_app = {}
                    deploy_app['appId'] = app_id
                    deploy_app['appVersion'] = appData.get('version')
                    deploy_app['appProviderId'] = appData.get('appProvider')
                    deploy_app['zoneInfo'] = {'zoneId': zone.get('edgeCloudZoneId')}
                    # Step 8: Deploy app at partner
                    deploy_app_response = federation_client.deploy_app_partner(federation_context_id=zone.get('fedContextId'), body=deploy_app, token = fed_token)
                    return deploy_app_response
                else:
                    return onboard_app_response
           else:
               return create_artefact_response 

       
       logger.info(f"Preparing to send deployment request to SRM for appId={app_id}")
       
       print("\n === Preparing Deployment Request ===")
       print(f" Endpoint: {pi_edge_client.base_url}/deployedServiceFunction")
       print(f" Headers: {pi_edge_client._get_headers()}")
       print(f"Payload: {body}")
       print("=== End of Deployment Request ===\n")
       
       try:
          response = pi_edge_client.deploy_service_function(data=body)
          
          if isinstance(response, dict) and "error" in response:
              logger.warning(f"Failed to deploy service function: {response}")
              return jsonify({
                  "warning": "Deployment not completed (SRM service unreachable)",
                  "details": response
                  
              }), 202
              
          logger.info(f"Deployment response from SRM: {response}")
       except Exception as inner_error:
           logger.error(f"Exception while trying to deploy to SRM: {inner_error}")
           return jsonify({
               "warning": "SRM backend unavailable. Deployment request was built correctly.",
               "details": str(inner_error)
           }),202
       return response   
    #    return jsonify({"message": f"Application {app_id} instantiation accepted"}), 202
    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        return jsonify({"error": "Validation error", "details": str(e)}), 400
    except Exception as e:
        logger.error(f"Unexpected error in create_app_instance:{str(e)}")
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500   

def get_app_instance(app_id=None, x_correlator=None, app_instance_id=None, region=None):
    """
    Retrieve application instances from the database.
    Supports filtering by app_id, app_instance_id, and region.
    """
    try:
        instances = None
        pi_edge_client_factory = PiEdgeAPIClientFactory()
        pi_edge_client = pi_edge_client_factory.create_pi_edge_api_client()

        if app_id is None and app_instance_id is None:
            instances = pi_edge_client.get_app_instances()

        if not instances:
            return jsonify({
                "status": 404,
                "code": "NOT_FOUND",
                "message": "No application instances found for the given parameters."
            }), 404

        return jsonify({"appInstanceInfo": instances}), 200

    except Exception as e:
        logger.exception("Failed to retrieve app instances")
        return jsonify({
            "status": 500,
            "code": "INTERNAL",
            "message": f"Internal server error: {str(e)}"
        }), 500


def delete_app_instance(appInstanceId: str, x_correlator=None):
    """
    Terminate an Application Instance

    - Removes a specific app instance from the database.
    - Returns 204 if deleted, 404 if not found.
    """
    try:
        pi_edge_client_factory = PiEdgeAPIClientFactory()
        pi_edge_client = pi_edge_client_factory.create_pi_edge_api_client()
        response = pi_edge_client.delete_app_instance(appInstanceId)
        return jsonify({'result': response.text, 'status': response.status_code})

    except Exception as e:
        return (
            jsonify({
                "status": 500,
                "code": "INTERNAL",
                "message": f"Internal server error: {str(e)}"
            }),
            500,
        )
