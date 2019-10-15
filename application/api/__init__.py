"""
Init Functions for API
"""
from application import app

@app.errorhandler(401)
def custom401(error):
    """ Custom 401 API Response """
    return {'status' : 401, 'message' : error}, 401

@app.after_request
def apply_headers(response):
    """ Additional Headers """
    if app.config.get('APPLY_HEADERS'):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] =\
                        "Origin, x-access-token, Content-Type, Accept"
    return response
