import pytest
from flask_awscognito.services.cognito_service import CognitoService
from flask_awscognito.exceptions import FlaskAWSCognitoError


@pytest.mark.usefixtures("set_env")
def test_base_url(user_pool_id, user_pool_client_id, cognito_idp):
    cognito = CognitoService(user_pool_id, user_pool_client_id, 'redirect', cognito_idp)
    assert cognito.base_url == 'https://test_domain_name.auth.eu-west-1.amazoncognito.com'


def test_no_region(user_pool_id, user_pool_client_id, cognito_idp):
    with pytest.raises(FlaskAWSCognitoError):
        CognitoService(user_pool_id, user_pool_client_id, 'redirect', cognito_idp)


@pytest.mark.usefixtures("set_env")
def test_sign_in_url(user_pool_id, user_pool_client_id, cognito_idp):
    cognito = CognitoService(user_pool_id, user_pool_client_id, 'http://redirect/url', cognito_idp)
    assert cognito.get_sign_in_url() == 'https://test_domain_name.auth.eu-west-1.amazoncognito.com' \
                                        '/login?response_type=code&' \
                                        'client_id=545isk1een1lvilb9en643g3vd&' \
                                        'redirect_uri=http%3A//redirect/url&' \
                                        'state=dc0de448b88af41d1cd06387ac2d5102'


@pytest.mark.usefixtures("set_env")
def test_exchange_code_for_token(user_pool_id, user_pool_client_id, cognito_idp, token_endpoint_request):
    cognito = CognitoService(user_pool_id, user_pool_client_id, 'http://redirect/url', cognito_idp)
    token = cognito.exchange_code_for_token(code='test_code', requests_client=token_endpoint_request)
    assert token == 'test_access_token'
