"""
Proxy project settings

Modify the below constants before building and running the application
to change the configuration of the project.
"""

#
# token settings
#
JWT_KEY = 'a9ddbcaba8c0ac1a0a812dc0c2f08514b23f2db0a68343cb8199ebb38a' \
    '6d91e4ebfb378e22ad39c2d01d0b4ec9c34aa91056862ddace3fbbd6852ee60c36acbf'
JWT_ALGO = 'HS512'
#
# proxy settings
#
PROXY_HOST = "0.0.0.0"
PROXY_PORT = 8080
PROXY_STATUS_PATH = "/status"
PROXY_ENDPOINT = "https://reqres.in"
PROXY_JWT_HEADER = "x-my-jwt"
#
# testing settings
#
PROXY_URL = "http://127.0.0.1"
TEST_DEBUG = True
