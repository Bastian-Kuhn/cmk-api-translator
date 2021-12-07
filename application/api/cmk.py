"""
Enpoints
"""
# pylint: disable=function-redefined
# pylint: disable=no-self-use
# pylint: disable=no-member
# pylint: disable=too-few-public-methods
import urllib.parse
from json.decoder import JSONDecodeError
from flask import request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

from flask_restplus import Namespace, Resource, fields
import requests
from application import app

API = Namespace('cmk')


ACK_DATA = API.model('acknowledgment', {
    "QUELLE" : fields.String,
    "QUELLEID": fields.String,
    "ZIEL" : fields.String,
    "ZIELID" : fields.String,
})


AUTH = HTTPBasicAuth()

@AUTH.verify_password
def verify_password(username, password):
    if username in app.config['API_USERS']:
        cfg_password = generate_password_hash(app.config['API_USERS'][username])
        return check_password_hash(cfg_password, password)
    return False

def create_payload(data):
    """
    Create a String with URL Payloads to set ACK
    """
    payload = {
        '_ack_comment' : "Ticket: {}".format(data['QUELLEID']),
        '_secret' : app.config['CMK_SECRET'],
        '_username' : app.config["CMK_USER"],

    }
    source_parts = data['ZIELID'].split('|')
    if len(source_parts) == 2:
        # Host Down
        payload['view_name'] = 'hoststatus'
    elif len(source_parts) == 3:
        payload['service'] = source_parts[2]
        payload['view_name'] = 'service'
        #service down
    else:
        raise ValueError("invalid id")

    payload['site'] = source_parts[0]
    payload['host'] = source_parts[1]

    return "&".join([x+"="+urllib.parse.quote(y) for x, y in payload.items()])


@API.route('status/')
class StatusAPI(Resource):
    """
    Status API
    """

    @API.expect(ACK_DATA, validate=True)
    @AUTH.login_required
    def post(self):
        """
        Check if a Error still exists
        """
        try:
            payload_str = create_payload(request.json)

            url = "{url}check_mk/view.py?output_format=json&{pl}".format(url=app.config['CMK_URL'],
                                                                         pl=payload_str)
            # The thing is that cmk not has
            # prober return status codes here,
            # so we cannot make nothing...
            response = requests.get(url, verify=app.config['SSL_VERIFY'])
            json_raw = response.json()
            data = dict(zip(json_raw[0], json_raw[1]))
            solved = True
            if 'service_state' in data:
                if data['service_state'] != "OK" and data['svc_in_downtime'] == 'no':
                    solved = False
            else:
                if data['host_state'] != "UP" and data['host_in_downtime'] == 'no':
                    solved = False
        except JSONDecodeError:
            return {"status": str(response.text)}
        except (ValueError, IndexError) as msg:
            return {"status" :str(msg)}, 500

        return {"problem_solved" : solved}, 200

@API.route('ack/')
class AckApi(Resource):
    """
    Acknowledgement API
    """

    @API.expect(ACK_DATA, validate=True)
    @AUTH.login_required
    def post(self):
        """
        Set ACK on Host or Service
        """
        try:
            payload_str = create_payload(request.json)

            url = "{url}check_mk/view.py?_acknowledge=Acknowledge&_do_actions=yes"\
            "&_do_confirm=yes&_transid=-1&{pl}".format(url=app.config['CMK_URL'],
                                                       pl=payload_str)
            # The thing is that cmk not has
            # prober return status codes here,
            # so we cannot make nothing...
            requests.get(url, verify=app.config['SSL_VERIFY'])
        except (ValueError, IndexError) as msg:
            return {"status" :str(msg)}, 500

        return {"status" : "success"}, 200
