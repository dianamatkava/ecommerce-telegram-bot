def generate_url(path: list, params: dict):
    url = '/'.join(list(filter(None, path)))
    param = str()
    for key, value in params.items():
        param = param + '='.join([key, str(value)]) + '&'
    return '?'.join([url, param])[0:-1]