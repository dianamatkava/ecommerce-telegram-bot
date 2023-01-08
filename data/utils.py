def generate_url(path: list, params: dict = None):
    url = '/'.join(list(filter(None, path)))
    if params:
        param = str()
        for key, value in params.items():
            param += '='.join([key, str(value)]) + '&'
        return '?'.join([url, param])[0:-1]
    return url