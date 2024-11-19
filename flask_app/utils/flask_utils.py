import json

from flask_app.constants.flask_constants import OCTET_STREAM


def custom_response(message: str, response_code: int):
    return json.loads(f'{{"message":"{message}"}}'), response_code, OCTET_STREAM