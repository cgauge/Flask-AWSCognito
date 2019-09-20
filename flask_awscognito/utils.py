from functools import wraps
from botocore.exceptions import BotoCoreError, ClientError
from flask_awscognito.exceptions import FlaskAWSCognitoError
from flask_awscognito.constants import HTTP_HEADER
from hashlib import md5


def catch_boto_exceptions(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except (BotoCoreError, ClientError) as e:
            raise FlaskAWSCognitoError(str(e)) from e
    return wrapped


def extract_access_token(request_headers):
    access_token = None
    auth_header = request_headers.get(HTTP_HEADER)
    if auth_header and ' ' in auth_header:
        _, access_token = auth_header.split()
    return access_token


def get_state(user_pool_id, user_pool_client_id):
    return md5(f'{user_pool_client_id}:{user_pool_id}'.encode('utf-8')).hexdigest()
