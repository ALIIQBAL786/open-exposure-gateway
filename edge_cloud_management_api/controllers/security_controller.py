import os
from jose import JWTError, jwt
from werkzeug.exceptions import Unauthorized

def decode_token(token:str):
    JWT_ISSUER = os.environ.get('JWT_ISSUER')
    PUBLIC_KEY = os.environ.get('JWT_PUBLIC_KEY')
    try:
        return jwt.decode(token, key=PUBLIC_KEY, algorithms=["RS256"], issuer=JWT_ISSUER)
    except JWTError as e:
        raise Unauthorized from e
    
def check_oAuth2ClientCredentials(token):
    return {'scopes': ['fed-mgmt'], 'uid': 'test_value'}


def validate_scope_oAuth2ClientCredentials(required_scopes, token_scopes):
    return set(required_scopes).issubset(set(token_scopes))
