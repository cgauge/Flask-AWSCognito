"""
Flask-AWSCognito
-------------

User authentication with AWS Cognito for Flask
"""
from setuptools import setup


setup(
    name='Flask-AWSCognito',
    version='1.0',
    url='https://github.com/cgauge/Flask-AWSCognito/',
    license='BSD',
    author='CustomerGauge',
    author_email='tech@customergauge.com',
    description='Authenticate users with AWS Cognito',
    long_description=__doc__,
    py_modules=['flask_awscognito'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'boto3',
        'jose',
        'requests'
    ],
    tests_require=[
        'pytest',
        'pytest-mock',
        'pytest-flask'
        ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
