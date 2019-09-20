import os
import boto3

from urllib.parse import quote
import requests
from flask_awscognito.utils import catch_boto_exceptions, get_state
from flask_awscognito.exceptions import FlaskAWSCognitoError


class CognitoService:
    def __init__(self, user_pool_id, user_pool_client_id, redirect_url, cognito_idp_client=None):
        self.user_pool_id = user_pool_id
        self.user_pool_client_id = user_pool_client_id
        self.redirect_url = redirect_url
        if not cognito_idp_client:
            cognito_idp_client = boto3.client('cognito-idp')
        self.cognito_idp_client = cognito_idp_client
        self._find_base_url()

    @catch_boto_exceptions
    def _find_base_url(self):
        response = self.cognito_idp_client.describe_user_pool(UserPoolId=self.user_pool_id)
        domain = response['UserPool']['Domain']
        region = os.getenv('AWS_DEFAULT_REGION')
        if not region:
            raise FlaskAWSCognitoError('No AWS region provided')

        self.base_url = f'https://{domain}.auth.{region}.amazoncognito.com'

    def get_sign_in_url(self):
        quoted_redirect_url = quote(self.redirect_url)
        state = get_state(self.user_pool_id, self.user_pool_client_id)
        full_url = f'{self.base_url}/login' \
                   f'?response_type=code' \
                   f'&client_id={self.user_pool_client_id}' \
                   f'&redirect_uri={quoted_redirect_url}' \
                   f'&state={state}'
        return full_url

    def exchange_code_for_token(self, code, requests_client=None):
        # TODO If the client was issued a secret, the client must pass its client_id and
        #  client_secret in the authorization header through Basic HTTP authorization.
        #  The secret is Basic Base64Encode(client_id:client_secret).
        token_url = f'{self.base_url}/oauth2/token'
        data = {'code': code,
                'redirect_uri': self.redirect_url,
                'client_id': self.user_pool_client_id,
                'grant_type': 'authorization_code'}
        try:
            if not requests_client:
                requests_client = requests.post
            response = requests_client(token_url, data=data)
            response_json = response.json()
        except requests.exceptions.RequestException as e:
            raise FlaskAWSCognitoError(str(e)) from e
        access_token = response_json['access_token']
        return access_token
