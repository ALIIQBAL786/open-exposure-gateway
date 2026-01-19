from flask import request, jsonify
import logging
import connexion
from requests.exceptions import Timeout, ConnectionError
from edge_cloud_management_api.managers.log_manager import logger
import requests
from edge_cloud_management_api.configs.env_config import config
from edge_cloud_management_api.services.storage_service import insert_zones
from edge_cloud_management_api.services.storage_service import insert_federation, get_fed, get_all_feds

from edge_cloud_management_api.services.federation_services import FederationManagerClientFactory

token_headers = {'Authorization': 'Basic b3JpZ2luYXRpbmctb3AtMTpkZDd2TndGcWpOcFl3YWdobEV3TWJ3MTBnMGtsV0RIYg==', 
                 'Content-Type': 'application/x-www-form-urlencoded'
                 }
data = {'grant_type': 'client_credentials',
        'scope': 'fed-mgmt'}
TOKEN_ENDPOINT = config.TOKEN_ENDPOINT


# Factory pattern
factory = FederationManagerClientFactory()
federation_client = factory.create_federation_client()


def create_federation():
    """POST /partner - Create federation with partner OP."""

    body = request.get_json()
    token = requests.post(TOKEN_ENDPOINT, headers=token_headers, data=data).json().get('access_token')
    response, code = federation_client.post_partner(body, token)
    fed = {'_id': response.get('federationContextId'), 'token': token}
    if code==200:
        provider = response.get('partnerOPFederationId')
        av_zones = response.get('offeredAvailabilityZones')
        zones_to_insert = []
        for zone in av_zones:
            inserted_item = {'_id': zone.get('zoneId'), 
                             'edgeCloudProvider': provider, 
                             'edgeCloudZoneId': zone.get('zoneId'), 
                             'edgeCloudZoneName': zone.get('geographyDetails'), 
                             'edgeCloudZoneStatus': 'unknown',
                             'isLocal': 'false',
                             'fedContextId': response.get('federationContextId')
                             }
            zones_to_insert.append(inserted_item)
        insert_zones(zones_to_insert)    
        insert_federation(fed)
    return response, code

def get_federation(federationContextId):
    """GET /{federationContextId}/partner - Get federation info."""
    fed = get_fed(federationContextId)
    if not fed:
        return 'Federation not found', 404
    else:
        token = fed.get('token')
        response, code = federation_client.get_partner(federationContextId, token)
        return response, code

def delete_federation(federationContextId):
    """DELETE /{federationContextId}/partner - Delete federation."""
    fed = get_fed(federationContextId)
    if not fed:
        return 'Federation not found', 404
    else:
        token = fed.get('token')
        response, code = federation_client.delete_partner(federationContextId, token)
        return response, code

def get_federation_context_ids():
    """GET /fed-context-id - Fetch federationContextId(s)."""
    feds = get_all_feds()
    if not feds:
        return 'Federation not found', 404
    else:
        token = feds[len(feds)-1].get('token')
        response, code = federation_client.get_federation_context_ids(token)
        return response, code
  

def onboard_application_to_partner(federationContextId):
    """POST /{federationContextId}/application/onboarding - Onboard app."""
    body = request.get_json()
    token = __get_token()
    result = federation_client.onboard_application(federationContextId, body, token)
    return jsonify(result)


def get_onboarded_app(federationContextId, appId):
    """GET /{federationContextId}/application/onboarding/app/{appId}"""

    token = __get_token()
    result = federation_client.get_onboarded_app(federationContextId, appId, token)
    return jsonify(result)


def delete_onboarded_app(federationContextId, appId):
    """DELETE /{federationContextId}/application/onboarding/app/{appId}"""

    token = __get_token()
    result = federation_client.delete_onboarded_app(federationContextId, appId, token)
    return jsonify(result)

'''---AVAILABILITY ZONE INFO SYNCHRONIZATION---'''

def request_zone_synch(federationContextId):
    token = __get_token()
    body = request.get_json()
    response = federation_client.request_zone_sync(federation_context_id=federationContextId, body=body, token=token)
    return jsonify(response)

def get_zone_resource_info(federationContextId, zoneId):
    token = __get_token()
    response = federation_client.get_zone_resource_info(federation_context_id=federationContextId, zone_id=zoneId, token=token)
    return jsonify(response)

def remove_zone_sync(federationContextId, zoneId):
    token = __get_token()
    response = federation_client.remove_zone_sync(federation_context_id=federationContextId, zone_id=zoneId, token=token)
    return jsonify(response)

def __get_token():
    bearer = connexion.request.headers['Authorization']
    token = bearer.split()[1]
    # __token = requests.post(TOKEN_ENDPOINT, headers=token_headers, data=data).json().get('access_token')
    return token

