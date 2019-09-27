[![Build Status](https://travis-ci.org/cgauge/Flask-AWSCognito.svg?branch=master)](https://travis-ci.org/cgauge/Flask-AWSCognito)
[![Documentation Status](https://readthedocs.org/projects/flask-awscognito/badge/?version=latest)](https://flask-awscognito.readthedocs.io/en/latest/?badge=latest)

# AWS Cognito for authentication in Flask

Documentation https://flask-awscognito.readthedocs.io

## Example App
```python
from flask import Flask, redirect, request, jsonify
from flask_awscognito import AWSCognitoAuthentication
app = Flask(__name__)

app.config['AWS_COGNITO_USER_POOL_ID'] = 'eu-west-1_Drvd8r4TM'
app.config['AWS_COGNITO_USER_POOL_CLIENT_ID'] = '545isk1een1lvilb9en643g3vd'
app.config['AWS_COGNITO_REDIRECT_URL'] = 'http://localhost:5000/aws_cognito_redirect'


aws_auth = AWSCognitoAuthentication(app)


@app.route('/')
@aws_auth.authentication_required
def index():
    claims = aws_auth.claims
    return jsonify({'claims': claims})


@app.route('/aws_cognito_redirect')
def aws_cognito_redirect():
    access_token = aws_auth.get_access_token(request.args)
    return jsonify({'access_token': access_token})


@app.route('/sign_in')
def sign_in():
    return redirect(aws_auth.get_sign_in_url())


if __name__ == '__main__':
    app.run(debug=True)

```

## ToDo
- token refresh
- client credentials flow for machine-to-machine interactions
- create user pool client with secret (token endpoint will need a header)
- logout
