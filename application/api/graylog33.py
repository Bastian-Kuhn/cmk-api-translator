"""
Enpoints
"""
# pylint: disable=function-redefined
# pylint: disable=no-self-use
# pylint: disable=no-member
# pylint: disable=too-few-public-methods
from flask import request
import datetime

from flask_restplus import Namespace, Resource, fields
from application import app

API = Namespace('graylog v33')



ALERT = API.model('v3.3-alert', {
    'event_defintion_id': fields.String
})


@API.route('/<string:token>')
class GraylogApi(Resource):
    """
    Status API
    """

    @API.expect(ALERT, validate=True)
    def post(self, token):
        """
        Check if a Error still exists
        """
        try:
            data_json = request.json
            print(data_json)
            out = open(app.config['MKEVENT_DEAMON_PATH'], "w")
            timestamp = datetime.now().strftime("%b %d %H:%M:%S")
            host = "srvlx120"
            msg = "There we go"
            out.write("<5>%s %s mail: %s\n" % (timestamp, host, msg))
            out.close()
        except PermissionError:
            return {"error": "Cannot Access Socket"}, 500 
        except (ValueError, IndexError) as msg:
            return {"error" :str(msg)}, 500

        return {"message" : "added"}, 200
