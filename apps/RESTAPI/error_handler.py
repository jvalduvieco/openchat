import json

from flask import Response


def handle_invalid_usage(error: ValueError):
    status_code = 400
    response_body = {"application_error": {"status_code": status_code, "message": error.__str__()}}
    response = Response(response=json.dumps(response_body),
                        status=status_code,
                        mimetype='application/json'
                        )
    return response
