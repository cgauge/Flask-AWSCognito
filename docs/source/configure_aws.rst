===============
Prepare Cognito
===============

CloudFormation
--------------

The following  CloudFormation template will create

- User Pool, a directory of users

- User Pool Client - an entity that holds the configuration of authentication flow



.. code-block:: yaml

    AWSTemplateFormatVersion: "2010-09-09"
    Description: Cognito Stack

    Parameters:
      Domain:
        Type: String
        Description: Unique Name for Cognito Resources
      SignInCallback:
        Type: String
        Description: Full URL to be called after used is signed in

    Resources:
      UserPool:
        Type: "AWS::Cognito::UserPool"
        Properties:
          UserPoolName: !Join ['-', [!Ref Domain, 'user-pool']]
          AutoVerifiedAttributes:
            - email
          Schema:
            - Name: email
              AttributeDataType: String
              Mutable: false
              Required: true

      PoolClientUser:
        Type: AWS::Cognito::UserPoolClient
        Description: Pool client to be used by users
        Properties:
          ClientName: !Join ['-', [!Ref Domain, 'cognito-user-pool-client']]
          UserPoolId: !Ref UserPool
          AllowedOAuthFlows:
            - code
          CallbackURLs:
            - !Ref SignInCallback
          AllowedOAuthFlowsUserPoolClient: true
          AllowedOAuthScopes:
            - email
            - openid
          SupportedIdentityProviders:
            - COGNITO

Domain
------

The template doesn't create a Domain (not supported by CLoudFormation as of December 2019)
so it should be created manually from console or through API calls.

.. image:: https://raw.githubusercontent.com/cgauge/Flask-AWSCognito/master/docs/img/cognito_domain.png

Both options - "Amazon Cognito domain" and "Your own domain" are supported. Don't forget to pass it
to Flask app config.


Redirect URL
------------

One of the stack parameters of the CloudFormation template is a redirect URL. It's a Flask endpoint users
will be redirected to after successful sign in (see **Usage**).


ID to pass to Flask
--------------------

After resources are created we need User Pool ID, User Pool Client ID and User Pool Client Secret
(not shown on the screenshots) to configure Flask:

.. image:: https://raw.githubusercontent.com/cgauge/Flask-AWSCognito/master/docs/img/poolid.png

.. image:: https://raw.githubusercontent.com/cgauge/Flask-AWSCognito/master/docs/img/clientid.png