import os
import pytest
from flask import Flask, jsonify
from flask_awscognito.exceptions import TokenVerifyError


@pytest.fixture
def set_env():
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-1"
    yield
    del os.environ["AWS_DEFAULT_REGION"]


@pytest.fixture
def user_pool_id():
    return "eu-west-1_Drvd8r4TM"


@pytest.fixture
def user_pool_client_id():
    return "545isk1een1lvilb9en643g3vd"


@pytest.fixture
def user_pool_client_secret():
    return "secret"


@pytest.fixture
def domain():
    return "cognito.domain.com"


@pytest.fixture
def region():
    return "eu-west-1"


@pytest.fixture
def token_endpoint_request(mocker):
    response = mocker.Mock()
    response.json = mocker.Mock(return_value={"access_token": "test_access_token"})
    request = mocker.Mock(return_value=response)
    return request


@pytest.fixture
def jwks():
    return {
        "keys": [
            {
                "alg": "RS256",
                "e": "AQAB",
                "kid": "2hQZJREoWZ/3A7hEYG+iIa7GJD+Jweu1caQ4rFrh2JM=",
                "kty": "RSA",
                "n": "m_FrYse7laSfIvHgKHVJzRknFnEjad79b0hrqQ1FoNOZ_JX5_15lSnHy0gPM542ZZ_cjCe6tbEavz4dI3g0CxZRW6esjXzRefVAuphilpQ1gmQDjASa6Qg2LqUS1Hd04m9UGSJo9vdG1KRsOK-MXGaV5EglKaTcINcVs31-B5R53rjuwTEcWpMlYb9VRq86VUdGEzH4I74sa6NYo3dSftL9N0ghH2lq0I2l2taVCH7FUk3phOeksNyTQgxnWQ-pGYzqpZOcZmEEdQMT3fjd4_pcqXSYrB3lmSN0nXxorq1RGmkRRQ3d70-Veyh4KvU-f_VzIdwIc5yLOzf3RaHMvFw",
                "use": "sig",
            },
            {
                "alg": "RS256",
                "e": "AQAB",
                "kid": "pv5k2Fdq+5uVgcb4jrgA76H7iVGvAO4uOmhpCheqTDo=",
                "kty": "RSA",
                "n": "pFToxHflSw-b8kfjaTERryoHdI4D1NaFCCNkNW1qaPSVp3FYZj4TzD3giF-XrnL0YgW_EpLs02mFWqHexgYfN-vJNOvbreT0wsmnzBoK2SlSKWqh70OBF26eVmmNCqMfRdNoP2QcqcagoKFRUkaxhC4TdVzPzb7l-xOnXrqsQlKCsR7ULuxYzBoRbSDJSq2YosE228Fq8ysMScle5i07fFUjpqnL3Yw1GQ3FPuBHYu5McAqLe1d_rRg2ER0FjVSggFut-3XICfe8Km8MCqglmnNT60RZo-ibsEXmN8zu2sJumyGLkGEDHJOf1VwKIdABWIey7UTlI2eYlqZRET04nw",
                "use": "sig",
            },
        ]
    }


@pytest.fixture
def jwks_endpoint_request(mocker, jwks):
    response = mocker.Mock()
    response.json = mocker.Mock(return_value=jwks)
    request = mocker.Mock(return_value=response)
    return request


@pytest.fixture
def app(user_pool_id, user_pool_client_id, user_pool_client_secret, region, domain):
    test_app = Flask(__name__)

    test_app.config["AWS_COGNITO_USER_POOL_ID"] = user_pool_id
    test_app.config["AWS_COGNITO_USER_POOL_CLIENT_ID"] = user_pool_client_id
    test_app.config["AWS_COGNITO_USER_POOL_CLIENT_SECRET"] = user_pool_client_secret
    test_app.config["AWS_DEFAULT_REGION"] = region
    test_app.config["AWS_COGNITO_DOMAIN"] = domain
    test_app.config[
        "AWS_COGNITO_REDIRECT_URL"
    ] = "http://localhost:5000/aws_cognito_redirect"
    return test_app


@pytest.fixture
def cognito_service_test_factory(mocker):
    return mocker.Mock()


@pytest.fixture
def token_service_test_factory(mocker):
    token_service = mocker.Mock()
    token_service.verify = verify
    return mocker.Mock(return_value=token_service)


def verify(token):
    if token != "good_token":
        raise TokenVerifyError("test")


@pytest.fixture
def test_view():
    def view():
        return jsonify({"data": 123})

    return view
