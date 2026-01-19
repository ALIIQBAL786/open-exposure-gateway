#from pydantic import BaseModel, HttpUrl, Field , UUID4
#from typing import Any, List, Optional
#from enum import Enum
# from ipaddress import IPv4Address, IPv6Address
#from edge_cloud_management_api.models.edge_cloud_models import EdgeCloudZone


from pydantic import BaseModel, HttpUrl, Field, UUID4
from typing import Any, List, Optional
from enum import Enum
from edge_cloud_management_api.models.edge_cloud_models import EdgeCloudZone  # <-- you should IMPORT this properly

# --- Enums ---

class VisibilityType(str, Enum):
    VISIBILITY_EXTERNAL = "VISIBILITY_EXTERNAL"
    VISIBILITY_INTERNAL = "VISIBILITY_INTERNAL"


class AppInstanceStatus(str, Enum):
    ready = "ready"
    instantiating = "instantiating"
    failed = "failed"
    terminating = "terminating"
    unknown = "unknown"


class Protocol(str, Enum):
    TCP = "TCP"
    UDP = "UDP"
    ANY = "ANY"

# --- Model Definitions ---

class NetworkInterface(BaseModel):
    interfaceId: str = Field(..., pattern="^[A-Za-z][A-Za-z0-9_]{3,31}$")
    protocol: Protocol
    port: int  # 1-65535
    visibilityType: VisibilityType


class ComponentSpec(BaseModel):
    componentName: str
    networkInterfaces: List[NetworkInterface]


class AppRepo(BaseModel):
    class AppRepoAuthType(str, Enum):
        DOCKER = "DOCKER"
        HTTP_BASIC = "HTTP_BASIC"
        HTTP_BEARER = "HTTP_BEARER"
        NONE = "NONE"

    type: str  # PRIVATEREPO or PUBLICREPO
    imagePath: HttpUrl
    userName: Optional[str]
    credentials: Optional[str]  # max 128 characters
    authType: Optional[AppRepoAuthType]
    checksum: Optional[str]


class AppManifest(BaseModel):
    class PackageType(str, Enum):
        QCOW2 = "QCOW2"
        OVA = "OVA"
        CONTAINER = "CONTAINER"
        HELM = "HELM"

    class OperatingSystem(BaseModel):
        architecture: str  # x86_64, x86
        family: str  # UBUNTU, RHEL, COREOS, etc
        version: str
        license: str

    name: str = Field(..., pattern="^[A-Za-z][A-Za-z0-9_]{1,63}$")
    appProvider: str = Field(..., pattern="^[A-Za-z][A-Za-z0-9_]{7,63}$")
    version: str
    packageType: PackageType
    operatingSystem: Optional[OperatingSystem]
    appRepo: AppRepo
    requiredResources: Optional[Any]  # Could be KubernetesResources, ContainerResources, etc.
    componentSpec: List[ComponentSpec]


class AppZones(BaseModel):
    kubernetesClusterRef: Optional[UUID4]
    EdgeCloudZone: EdgeCloudZone


class AppInstance(BaseModel):
    appId: UUID4
    appZones: List[AppZones]

