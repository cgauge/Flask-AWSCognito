from flask_awscognito.services.token_service import TokenService
from flask_awscognito.services.cognito_service import CognitoService


def cognito_service_factory(
    user_pool_id,
    user_pool_client_id,
    user_pool_client_secret,
    redirect_url,
    client_state,
    region,
    domain,
):
    return CognitoService(
        user_pool_id,
        user_pool_client_id,
        user_pool_client_secret,
        redirect_url,
        client_state,
        region,
        domain,
    )


def token_service_factory(user_pool_id, user_pool_client_id, region):
    return TokenService(user_pool_id, user_pool_client_id, region)
