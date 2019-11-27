===================
Configure Flask app
===================

Flask app configuration should contain a number of Cognito paramaters.


.. code-block:: python

    app = Flask(__name__)

    app.config['AWS_DEFAULT_REGION'] = 'eu-west-1'
    app.config['AWS_COGNITO_DOMAIN'] = 'domain.com'
    app.config['AWS_COGNITO_USER_POOL_ID'] = 'eu-west-1_XXX'
    app.config['AWS_COGNITO_USER_POOL_CLIENT_ID'] = 'YYY'
    app.config['AWS_COGNITO_USER_POOL_CLIENT_SECRET'] = 'ZZZZ'
    app.config['AWS_COGNITO_REDIRECT_URL'] = 'http://localhost:5000/aws_cognito_redirect'

    aws_auth = AWSCognitoAuthentication(app)

