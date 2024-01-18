"""
Enpoints
"""
# pylint: disable=function-redefined
# pylint: disable=no-self-use
# pylint: disable=no-member
# pylint: disable=too-few-public-methods
from flask import request
from datetime import datetime
from dateutil.parser import parse as time_parse

from flask_restx import Namespace, Resource, fields
from application import app

API = Namespace('graylog v33')


EVENT = API.model('event', {
    'message': fields.String(required=True),
    'source': fields.String(required=True),
    'timestamp': fields.String(required=True, example="2020-09-10T14:10:53.220Z"),
})

ALERT = API.model('v3.3-alert', {
    'event': fields.Nested(EVENT)
})


@API.route('/<string:token>')
class GraylogApi(Resource):
    """
    Status API
    """

    @API.expect(ALERT, validate=True)
    def post(self, token):
        """
        Create EC Entry
        """
        try:
            if token != app.config['GRAYLOG_TOKEN']:
                raise ValueError("Invalid Token")
            data_json = request.json
            time_string = data_json['event']['timestamp']
            timestamp = time_parse(time_string).strftime("%b %d %H:%M:%S")
            msg = data_json['event']['message']
            host = data_json['event']['source']
            out = open(app.config['MKEVENT_DEAMON_PATH'], "w")
            out.write("<5>{ts} {host} graylog: {msg}\n".format(ts=timestamp, host=host, msg=msg))
            out.close()
        except PermissionError:
            return {"error": "Cannot Access Socket"}, 500
        except (ValueError, IndexError) as msg:
            return {"error" :str(msg)}, 500

        return {"message" : "added"}, 200
