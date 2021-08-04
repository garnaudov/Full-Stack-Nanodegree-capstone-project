import json
import os
from urllib.request import urlopen
from functools import wraps
from jose import jwt
from flask import request, abort


ASSISTANT_TOKEN = os.getenv('ASSISTANT_TOKEN')
DIRECTOR_TOKEN = os.getenv('DIRECTOR_TOKEN')
PRODUCER_TOKEN = os.getenv('PRODUCER_TOKEN')

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
ALGORITHMS = os.getenv('ALGORITHMS')
API_AUDIENCE = os.getenv('API_AUDIENCE')

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

    def __repr__(self):
        return 'class'+str(self.error)+" code "+str(self.status_code)+' what'

'''
 check_permissions(permission, payload) method
    @INPUTS
        permission: permission string (for example 'view:actors')
        payload: jwt payload /decoded/
    return AuthError if permissions is not in the payload array; otherwise returns true
'''

def check_permissions(permissions, payload):
    if 'permissions' not in payload:
        abort(400)
    if permissions not in payload['permissions']:
        return False
    return True

def get_token_auth_header():
    auth_header = request.headers.get('Authorization', None)
    if auth_header is None:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header not present'
        }, 401)
    auth_header = auth_header.split(' ')
    if len(auth_header) != 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Error with authorization header length.'
        }, 401)
    if auth_header[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header doesnt start with bearer!'
        }, 401)
    return auth_header[1]

'''
verify_decode_jwt(token) method
    @INPUTS
        token: JWT auth token with kid (string)

    returns the decoded payload from the token after verifying via Auth0 domain and validating the claims
    otherwise returns AuthError
'''

def verify_decode_jwt(auth_token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    unverified_header = jwt.get_unverified_header(auth_token)
    rsa_key = {}
    jwks = json.loads(jsonurl.read())
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
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
                auth_token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload


        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Claims are incorrect. Check again the audience and issuer.'
            }, 401)
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'The auth token is expired.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Cannot parse the authentication auth token.'
            }, 400)
    raise AuthError({
        'code': 'invalid_header',
                'description': 'Cannot find the appropriate key.'
    }, 401)
    return unverified_header

'''
@requires_auth(permission) decorator method
    @INPUTS
        permission: permission string (i.e. 'view:actors')
    returns the decorator which passes the decoded payload to the decorated method after getting, verifying and checking permissions
'''

def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth_token = get_token_auth_header()
            payload = verify_decode_jwt(auth_token)
            if not check_permissions(permission, payload):
                raise AuthError({
                    'code': 'invalid_header',
                    'description': 'The user doesnt have permissions to perform this step'
                }, 401)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator


