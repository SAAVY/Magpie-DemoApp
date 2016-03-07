IS_DEV = False

PORT_NUMBER = 8000

DEV_API_URL = "http://localhost:5000/website"
PROD_API_URL = "http://localhost:8002/website"


class StatusCode(object):
    OK = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500
