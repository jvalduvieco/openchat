def handle_invalid_usage(error: ValueError):
    response = error.__str__()
    return response, 400
