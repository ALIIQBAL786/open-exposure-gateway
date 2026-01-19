import requests
from edge_cloud_management_api.managers.log_manager import logger
from requests.exceptions import Timeout, ConnectionError
from edge_cloud_management_api.configs.env_config import config


proxies = {
    "http": config.HTTP_PROXY,
    "https": config.HTTP_PROXY,
}

class PiEdgeAPIClient:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.token = None
        

    def _get_proxy_session(self, session_proxies):
        session = requests.Session()
        session.proxies.update(session_proxies)
        return session

    def _authenticate(self):
        """
        Private method to login and obtain an authentication token.
        This is automatically called when headers are required and token is missing.
        """
        login_url = f"{self.base_url}/authentication"
        credentials = {"username": self.username, "password": self.password}

        try:
            response = self.requests_session.post(
                login_url,
                json=credentials,
                # proxies=proxies,
            )
            response.raise_for_status()

            self.token = response.json().get("token")
            if not self.token:
                raise ValueError("Login failed: No token found")
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err}")
        except Exception as err:
            logger.error(f"Error occurred: {err}")

    def _get_headers(self):
        """
        Helper function to return the authorization headers with token.
        If token is not available, automatically login.
        """
        #if not self.token:
         #   self._authenticate()

        return {
           # "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def get_service_functions_catalogue(self):
        """
        Get service function catalogue from the /serviceFunction endpoint.
        """
        url = f"{self.base_url}/serviceFunction"
        try:
            request_headers = self._get_headers()
            response = requests.get(url, headers=request_headers, verify=False)
            response.raise_for_status()
            service_functions = response.json()
            if isinstance(service_functions, list):
                return service_functions
            raise ValueError("Unexpected response from Service Resource manager")

        except Timeout:
            return {"error": "The request to the external API timed out. Please try again later."}

        except ConnectionError:
            return {"error": "Failed to connect to the external API service. Service might be unavailable."}

        except requests.exceptions.HTTPError as http_err:
            return {
                "error": f"HTTP error occurred: {http_err}.",
                "status_code": response.status_code,
            }

        except ValueError as val_err:
            return {"error": str(val_err)}

        except Exception as err:
            return {"error": f"An unexpected error occurred: {err}"}
        
        
    def submit_app(self, body):
        """
        Register app metadata to SRM
        """
        url = f"{self.base_url}/serviceFunction"
        try:
            request_headers = self._get_headers()
            response = requests.post(url, headers=request_headers, verify=False, json=body)
            response.raise_for_status()
            return response.json()
        except Timeout:
            return {"error": "The request to the external API timed out. Please try again later."}

        except ConnectionError:
            return {"error": "Failed to connect to the external API service. Service might be unavailable."}

        except requests.exceptions.HTTPError as http_err:
            return {
                "error": f"HTTP error occurred: {http_err}.",
                "status_code": response.status_code,
            }
        
    def get_app(self, appId):
        """
        Get app metadata from SRM
        """
        url = f"{self.base_url}/serviceFunction/"+appId
        try:
            request_headers = self._get_headers()
            response = requests.get(url, headers=request_headers, verify=False)
            response.raise_for_status()
            return response.json()
        except Timeout:
            return {"error": "The request to the external API timed out. Please try again later."}

        except ConnectionError:
            return {"error": "Failed to connect to the external API service. Service might be unavailable."}

        except requests.exceptions.HTTPError as http_err:
            return {
                "error": f"HTTP error occurred: {http_err}.",
                "status_code": response.status_code,
            }
        
    def delete_app(self, appId:str):
        """
        Remove app metadata from SRM
        """
        url = f"{self.base_url}/serviceFunction/"+appId
        try:
            response = requests.delete(url,headers=self._get_headers(), verify=False)
            response.raise_for_status()
            return response.text
        except Timeout:
            return {"error": "The request to the external API timed out. Please try again later."}

        except ConnectionError:
            return {"error": "Failed to connect to the external API service. Service might be unavailable."}

        except requests.exceptions.HTTPError as http_err:
            return {
                "error": f"HTTP error occurred: {http_err}.",
                "status_code": response.status_code,
            }

        except Exception as err:
            return {"error": f"An unexpected error occurred: {err}"}

    def deploy_service_function(self, data: dict):
        """
        Post data to the /deployedServiceFunction endpoint.
        """
        url = f"{self.base_url}/deployedServiceFunction"
        try:
            response = requests.post(url, json=data, headers=self._get_headers(), verify=False)
            response.raise_for_status()
            return response.json()
        except Timeout:
            return {"error": "The request to the external API timed out. Please try again later."}

        except ConnectionError:
            return {"error": "Failed to connect to the external API service. Service might be unavailable."}

        except requests.exceptions.HTTPError as http_err:
            return {
                "error": f"HTTP error occurred: {http_err}.",
                "status_code": response.status_code,
            }

        except Exception as err:
            return {"error": f"An unexpected error occurred: {err}"}
        

    def get_app_instances(self):
        """
        Retrieve all app instances.
        """
        url = f"{self.base_url}/deployedServiceFunction"
        try:
            response = requests.get(url, headers=self._get_headers(), verify=False)
            response.raise_for_status()
            return response.json()
        except Timeout:
            return {"error": "The request to the external API timed out. Please try again later."}

        except ConnectionError:
            return {"error": "Failed to connect to the external API service. Service might be unavailable."}

        except requests.exceptions.HTTPError as http_err:
            return {
                "error": f"HTTP error occurred: {http_err}.",
                "status_code": response.status_code,
            }
        

    def delete_app_instance(self, app_instance_id:str):
        """
        Remove app instance.
        """
        url = f"{self.base_url}/deployedServiceFunction/"+app_instance_id
        try:
            response = requests.delete(url, headers=self._get_headers(), verify=False)
            response.raise_for_status()
            return response
        except Timeout:
            return {"error": "The request to the external API timed out. Please try again later."}

        except ConnectionError:
            return {"error": "Failed to connect to the external API service. Service might be unavailable."}

        except requests.exceptions.HTTPError as http_err:
            return {
                "error": f"HTTP error occurred: {http_err}.",
                "status_code": response.status_code,
            }


    def edge_cloud_zones(self):
        """
        Get list of edge zones from /node endpoint.
        """
        url = f"{self.base_url}/node"
        #try:
        request_headers = self._get_headers()
        response = requests.get(url, headers=request_headers, verify=False)
        response.raise_for_status()
        nodes = response.json()
        if not nodes:
            raise ValueError("No edge nodes found")
        return nodes


    def edge_cloud_zone_details(self, zone_id):
        """
        Get list of edge zones from /node endpoint.
        """
        url = f"{self.base_url}/node/"+zone_id
        #try:
        request_headers = self._get_headers()
        response = requests.get(url, headers=request_headers, verify=False)
        response.raise_for_status()
        nodes = response.json()
        if not nodes:
            raise ValueError("No edge nodes found")
        return nodes     

    def create_qod_session(self, body:dict):

        url = f"{self.base_url}/sessions"
        request_headers = self._get_headers()
        response = requests.post(url, json=body, headers=request_headers,verify=False)
        response.raise_for_status()
        if response.status_code==200:
            return response.json()
        elif response.status_code==500:
            return response.content
        
            

    def get_qod_session(self, sessionId: str):

        url = f"{self.base_url}/sessions/"+sessionId
        request_headers = self._get_headers()
        response = requests.get(url, headers=request_headers,verify=False)
        response.raise_for_status()
        if response.status_code==200:
            return response.json()
        elif response.status_code==500:
            return response.content
        
        
    def delete_qod_session(self, sessionId: str):

        url = f"{self.base_url}/sessions/"+sessionId
        request_headers = self._get_headers()
        response = requests.delete(url, headers=request_headers,verify=False)
        response.raise_for_status()
        if response.status_code==200:
            return response.text
        elif response.status_code==500:
            return response.content

    def create_traffic_influence_resource(self, body_dict):
        url = f"{self.base_url}/traffic-influences"
        request_headers = self._get_headers()
        response = requests.post(url, json=body_dict, headers=request_headers,verify=False)
        response.raise_for_status()
        if response.status_code==200:
            return response.json()
        elif response.status_code==500:
            return response.content

    def delete_traffic_influence_resource(self, id: str):
        url = f"{self.base_url}/traffic-influences/"+id
        request_headers = self._get_headers()
        response = requests.delete(url, headers=request_headers,verify=False)
        response.raise_for_status()
        if response.status_code==200:
            return response.json()
        elif response.status_code==500:
            return response.content

    def get_traffic_influence_resource(self, id: str):
        url = f"{self.base_url}/traffic-influences/"+id
        request_headers = self._get_headers()
        response = requests.get(url, headers=request_headers,verify=False)
        response.raise_for_status()
        if response.status_code==200:
            return response.json()
        elif response.status_code==500:
            return response.content

    def get_all_traffic_influence_resources(self):
        url = f"{self.base_url}/traffic-influences/"
        request_headers = self._get_headers()
        response = requests.get(url, headers=request_headers,verify=False)
        response.raise_for_status()
        if response.status_code==200:
            return response.json()
        elif response.status_code==500:
            return response.content

class PiEdgeAPIClientFactory:
    """
    Factory class to create instances of PiEdgeAPIClient.
    """

    def __init__(self):
        self.default_base_url = config.SRM_HOST
        self.default_username = config.PI_EDGE_USERNAME
        self.default_password = config.PI_EDGE_PASSWORD

    def create_pi_edge_api_client(self, base_url=None, username=None, password=None):
        """
        Factory method to create a new SRMAPIClient instance.

        Args:
            base_url (str): The base URL for the SRM API. If None, the default is used.
            username (str): The username for authentication. If None, the default is used.
            password (str): The password for authentication. If None, the default is used.

        Returns:
            PiEdgeAPIClient: A new instance of the PiEdgeAPIClient.
        """
        if base_url is None:
            base_url = self.default_base_url
        if username is None:
            username = self.default_username
        if password is None:
            password = self.default_password

        return PiEdgeAPIClient(base_url=base_url, username=username, password=password)


if __name__ == "__main__":
    pi_edge_factory = PiEdgeAPIClientFactory()
    api_client = pi_edge_factory.create_pi_edge_api_client()

    edge_zones = api_client.edge_cloud_zones()
    logger.error("Edge zones:", edge_zones)
