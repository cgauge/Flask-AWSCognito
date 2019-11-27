import pytest
from flask_awscognito.services.cognito_service import CognitoService
from flask_awscognito.exceptions import FlaskAWSCognitoError


@pytest.mark.usefixtures("set_env")
def test_base_url(
    user_pool_id, user_pool_client_id, user_pool_client_secret, region, domain
):
    cognito = CognitoService(
        user_pool_id,
        user_pool_client_id,
        user_pool_client_secret,
        "redirect",
        region,
        domain,
    )
    assert cognito.domain == "https://" + domain


@pytest.mark.usefixtures("set_env")
def test_sign_in_url(
    user_pool_id, user_pool_client_id, user_pool_client_secret, region, domain
):
    cognito = CognitoService(
        user_pool_id,
        user_pool_client_id,
        user_pool_client_secret,
        "http://redirect/url",
        region,
        domain,
    )
    assert (
        cognito.get_sign_in_url() == f"https://{domain}"
        "/login?response_type=code&"
        "client_id=545isk1een1lvilb9en643g3vd&"
        "redirect_uri=http%3A//redirect/url&"
        "state=dc0de448b88af41d1cd06387ac2d5102"
    )


@pytest.mark.usefixtures("set_env")
def test_exchange_code_for_token(
    user_pool_id,
    user_pool_client_id,
    user_pool_client_secret,
    region,
    domain,
    token_endpoint_request,
):
    cognito = CognitoService(
        user_pool_id,
        user_pool_client_id,
        user_pool_client_secret,
        "http://redirect/url",
        region,
        domain,
    )
    token = cognito.exchange_code_for_token(
        code="test_code", requests_client=token_endpoint_request
    )
    assert token == "test_access_token"
