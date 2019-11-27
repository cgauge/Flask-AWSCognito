Authorization code grant
========================

The authorization code grant is the preferred method for authorizing end users. Instead of directly providing user pool tokens to an end user upon authentication, an authorization code is provided. This code is then sent to a custom application that can exchange it for the desired tokens. Because the tokens are never exposed directly to an end user, they are less likely to become compromised.

See AWS_ docs.
 .. _AWS: https://aws.amazon.com/blogs/mobile/understanding-amazon-cognito-user-pool-oauth-2-0-grants/


Diagram
-------

.. image:: https://raw.githubusercontent.com/cgauge/Flask-AWSCognito/master/docs/img/flask-cognito.png

Sign in
-------
A user opens AWS Cognito UI for:
 - sign up
 - registration confirmation (confirmation code is sent user's email address)
 - password reset
 - sign in

To get URL for sign in:

.. code-block:: python

    @app.route('/sign_in')
    def sign_in():
        return redirect(aws_auth.get_sign_in_url())


Redirect
--------

After successful sign in the user is redirected to Flask endpoint
(see Redirect URL in **Prepare Cognito**)

Endpoint's example code:

.. code-block:: python

    @app.route('/aws_cognito_redirect')
    def aws_cognito_redirect():
        access_token = aws_auth.get_access_token(request.args)
        return jsonify({'access_token': access_token})


Authorize
---------

Now the client has access token and it should present it to any endpoint
that requires authorization:

.. code-block:: python

    @app.route('/')
    @aws_auth.authentication_required
    def index():
        claims = aws_auth.claims # or g.cognito_claims
        return jsonify({'claims': claims})

Authenticated user data is available through plugins attribute `claims`. Claims are also
available through the `g` object attribute `cognito_claims`


Client
------

A client could be an JavaScript app, running in a user browser.
It should:
- remember access token it got as a Redirect URL response
- present a token in each request to Flask endpoint using a HTTP header
like ``Authorization: Basic TOKEN_HERE``
