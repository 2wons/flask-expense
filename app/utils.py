from flask import Response

def HXRedirect(url):
    response = Response()
    response.headers["hx-redirect"] = url
    return response