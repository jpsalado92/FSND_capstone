import configparser
import json
from functools import wraps
from urllib.request import urlopen

from flask import request
from jose import jwt

config = configparser.ConfigParser()
config_file = "secrets.cfg"
config.read(config_file)

AUTH0_DOMAIN = config['AUTH0']['AUTH0_DOMAIN']
API_AUDIENCE = config['AUTH0']['API_AUDIENCE']
ALGORITHMS = ['RS256']


class AuthError(Exception):
    """
    AuthError Exception
    A standardized way to communicate auth failure modes
    """

    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    """
    Gets the header from the request and returns the JWT token part of the header.
    Raises an AuthError if no header is present or if it is malformed.
    """
    if 'Authorization' not in request.headers:
        raise AuthError(
            {'code': 'unauthorized', 'description': 'Authorization header was not found.'},
            401
        )

    auth_header = request.headers["Authorization"]
    header_parts = auth_header.split(' ')

    if len(header_parts) != 2:
        raise AuthError(
            {'code': 'unauthorized', 'description': 'Malformed header.'},
            401
        )

    if header_parts[0].lower() != "bearer":
        raise AuthError(
            {'code': 'unauthorized', 'description': 'Bearer not found.'},
            401
        )

    return header_parts[1]


def check_permissions(permission, payload):
    """
    permission: string permission (i.e. 'post:drink')
    payload: decoded jwt payload
    Raises an AuthError if the requested permission string is not in the payload permissions array return true otherwise
    """
    if 'permissions' not in payload:
        raise AuthError(
            {'code': 'invalid_claims', 'description': 'Permissions not included in JWT.'}
            , 400
        )
    if permission not in payload['permissions']:
        raise AuthError(
            {'code': 'unauthorized', 'description': 'Permission not found.'},
            401)
    return True


def verify_decode_jwt(token):
    """
    :param token: a json web token (string)
    :return:
    """
    # Auth0 exposes a JWKS endpoint for each tenant, which is found at https://YOUR_DOMAIN/.well-known/jwks.json.
    # This endpoint will contain the JWK used to sign all Auth0-issued JWTs for this tenant.
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}

    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        # Validate the claims
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

        if rsa_key:
            try:
                payload = jwt.decode(
                    token,  # Decode the payload from the token
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer='https://' + AUTH0_DOMAIN + '/'
                )
                # Return the decoded payload
                return payload

            except jwt.ExpiredSignatureError:
                raise AuthError({
                    'code': 'token_expired',
                    'description': 'Token expired.'
                }, 401)

            except jwt.JWTClaimsError:
                raise AuthError({
                    'code': 'invalid_claims',
                    'description': 'Incorrect claims. Please, check the audience and issuer.'
                }, 401)

            except Exception:
                raise AuthError({
                    'code': 'invalid_header',
                    'description': 'Unable to parse authentication token.'
                }, 400)

        raise AuthError({
            'code': 'invalid_header',
            'description': 'Unable to find the appropriate key.'
        }, 400)


def requires_auth(permission=''):
    """
    :param permission: string permission (i.e. 'post:drink')
    :return:
    """

    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator
