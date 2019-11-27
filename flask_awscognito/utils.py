from flask_awscognito.constants import HTTP_HEADER
from hashlib import md5


def extract_access_token(request_headers):
    access_token = None
    auth_header = request_headers.get(HTTP_HEADER)
    if auth_header and " " in auth_header:
        _, access_token = auth_header.split()
    return access_token


def get_state(user_pool_id, user_pool_client_id):
    return md5(f"{user_pool_client_id}:{user_pool_id}".encode("utf-8")).hexdigest()
