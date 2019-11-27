import pytest
from flask_awscognito import AWSCognitoAuthentication


@pytest.mark.usefixtures("set_env")
def test_get_access_token(
    app, cognito_service_test_factory, token_service_test_factory
):
    plugin = AWSCognitoAuthentication(
        app,
        _token_service_factory=token_service_test_factory,
        _cognito_service_factory=cognito_service_test_factory,
    )
    with app.app_context():
        assert plugin.token_service
        assert plugin.cognito_service
        req_args = {"code": "code", "state": "dc0de448b88af41d1cd06387ac2d5102"}
        plugin.get_access_token(req_args)
        plugin.cognito_service.exchange_code_for_token.assert_called_with("code")


@pytest.mark.usefixtures("set_env")
def test_no_auth(
    app, cognito_service_test_factory, token_service_test_factory, client, test_view
):
    plugin = AWSCognitoAuthentication(
        app,
        _token_service_factory=token_service_test_factory,
        _cognito_service_factory=cognito_service_test_factory,
    )
    app.route("/")(plugin.authentication_required(test_view))
    res = client.get("/")
    assert res.status_code == 401
    assert res.json == {"message": "test"}


@pytest.mark.usefixtures("set_env")
def test_no_auth_bad_token(
    app, cognito_service_test_factory, token_service_test_factory, client, test_view
):
    plugin = AWSCognitoAuthentication(
        app,
        _token_service_factory=token_service_test_factory,
        _cognito_service_factory=cognito_service_test_factory,
    )
    app.route("/")(plugin.authentication_required(test_view))
    res = client.get("/", headers={"Authorization": "Bearer bad_token"})
    assert res.status_code == 401
    assert res.json == {"message": "test"}


@pytest.mark.usefixtures("set_env")
def test_auth(
    app, cognito_service_test_factory, token_service_test_factory, client, test_view
):
    plugin = AWSCognitoAuthentication(
        app,
        _token_service_factory=token_service_test_factory,
        _cognito_service_factory=cognito_service_test_factory,
    )
    app.route("/")(plugin.authentication_required(test_view))
    res = client.get("/", headers={"Authorization": "Bearer good_token"})
    assert res.status_code == 200
    assert res.json == {"data": 123}
