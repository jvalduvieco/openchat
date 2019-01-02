def handle_invalid_usage(error: ValueError):
    status_code = 400
    response_body = """{"application_error": {"status_code": %d ,"message": "%s"}}""" % (status_code, error.__str__())
    return response_body, status_code
