===================
Configure Flask app
===================

Presumably Flask is running on AWS and `boto3` is configured with
proper credentials automatically.

.. code-block:: python

    app = Flask(__name__)

    app.config['AWS_COGNITO_USER_POOL_ID'] = 'eu-west-1_XXXXX'
    app.config['AWS_COGNITO_USER_POOL_CLIENT_ID'] = '31v4XXXXXX'
    app.config['AWS_COGNITO_REDIRECT_URL'] = 'https://example.com/aws_cognito_redirect'

    aws_auth = AWSCognitoAuthentication(app)

