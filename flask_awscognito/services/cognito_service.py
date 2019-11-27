from base64 import b64encode
from urllib.parse import quote
import requests
from flask_awscognito.utils import get_state
from flask_awscognito.exceptions import FlaskAWSCognitoError


class CognitoService:
    def __init__(
        self,
        user_pool_id,
        user_pool_client_id,
        user_pool_client_secret,
        redirect_url,
        region,
        domain,
    ):
        self.user_pool_id = user_pool_id
        self.user_pool_client_id = user_pool_client_id
        self.user_pool_client_secret = user_pool_client_secret
        self.redirect_url = redirect_url
        self.region = region
        if domain.startswith("https://"):
            self.domain = domain
        else:
            self.domain = f"https://{domain}"

    def get_sign_in_url(self):
        quoted_redirect_url = quote(self.redirect_url)
        state = get_state(self.user_pool_id, self.user_pool_client_id)
        full_url = (
            f"{self.domain}/login"
            f"?response_type=code"
            f"&client_id={self.user_pool_client_id}"
            f"&redirect_uri={quoted_redirect_url}"
            f"&state={state}"
        )
        return full_url

    def exchange_code_for_token(self, code, requests_client=None):
        token_url = f"{self.domain}/oauth2/token"
        data = {
            "code": code,
            "redirect_uri": self.redirect_url,
            "client_id": self.user_pool_client_id,
            "grant_type": "authorization_code",
        }
        headers = {}
        if self.user_pool_client_secret:
            secret = b64encode(
                f"{self.user_pool_client_id}:{self.user_pool_client_secret}".encode(
                    "utf-8"
                )
            ).decode("utf-8")
            headers = {"Authorization": f"Basic {secret}"}
        try:
            if not requests_client:
                requests_client = requests.post
            response = requests_client(token_url, data=data, headers=headers)
            response_json = response.json()
        except requests.exceptions.RequestException as e:
            raise FlaskAWSCognitoError(str(e)) from e
        if "access_token" not in response_json:
            raise FlaskAWSCognitoError(
                f"no access token returned for code {response_json}"
            )
        access_token = response_json["access_token"]
        return access_token
