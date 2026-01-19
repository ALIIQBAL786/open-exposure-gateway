import os
from pydantic.v1 import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Configuration(BaseSettings):
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    SRM_HOST: str = os.getenv("SRM_HOST", "http://localhost:8989")
    PI_EDGE_USERNAME: str = os.getenv("PI_EDGE_USERNAME", "admin")
    PI_EDGE_PASSWORD: str = os.getenv("PI_EDGE_PASSWORD", "password")
    HTTP_PROXY: str = os.getenv("HTTP_PROXY", "")
    FEDERATION_MANAGER_HOST: str = os.getenv("FEDERATION_MANAGER_HOST", "http://localhost:8989")
    TOKEN_ENDPOINT: str = os.getenv('TOKEN_ENDPOINT', "http://localhost:8081/token")
    PARTNER_API_ROOT: str = os.getenv('PARTNER_API_ROOT', "http://localhost:8080")


config = Configuration()
