from flask_awscognito.services.token_service import TokenService
from flask_awscognito.services.cognito_service import CognitoService


def cognito_service_factory(user_pool_id, user_pool_client_id, redirect_url):
    return CognitoService(user_pool_id, user_pool_client_id, redirect_url)


def token_service_factory(user_pool_id, user_pool_client_id):
    return TokenService(user_pool_id, user_pool_client_id)
