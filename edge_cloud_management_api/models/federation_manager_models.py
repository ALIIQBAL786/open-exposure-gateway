from pydantic import BaseModel #Field
from typing import List, Optional


class MobileNetworkIds(BaseModel):
    mncs: List[str]
    mcc: str


class FixedNetworkIds(BaseModel):
    __root__: List[str]


class CallbackCredentials(BaseModel):
    tokenUrl: str
    clientId: str
    clientSecret: str


class ServiceEndpoint(BaseModel):
    ipv4Addresses: Optional[List[str]] = None
    ipv6Addresses: Optional[List[str]] = None
    port: Optional[int] = None
    fqdn: Optional[str] = None


class ZoneDetails(BaseModel):
    geographyDetails: str
    zoneId: str
    geolocation: str


class FederationRequestData(BaseModel):
    origOPFederationId: str
    origOPCountryCode: Optional[str]
    origOPMobileNetworkCodes: Optional[MobileNetworkIds]
    origOPFixedNetworkCodes: Optional[List[str]]
    initialDate: str
    partnerStatusLink: str
    partnerCallbackCredentials: Optional[CallbackCredentials]


class FederationResponseData(BaseModel):
    federationContextId: str
    partnerOPFederationId: str
    partnerOPCountryCode: Optional[str]
    partnerOPMobileNetworkCodes: Optional[MobileNetworkIds]
    partnerOPFixedNetworkCodes: Optional[List[str]]
    offeredAvailabilityZones: Optional[List[ZoneDetails]]
    platformCaps: List[str]
    edgeDiscoveryServiceEndPoint: Optional[ServiceEndpoint]
    lcmServiceEndPoint: Optional[ServiceEndpoint]
