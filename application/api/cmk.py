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

from flask_restx import Namespace, Resource, fields
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


def get_job(data):
    """
    Determine by API Data what is to do
    """
    source_parts = data['ZIELID'].split('|')
    job = False
    service_name = False
    if len(source_parts) == 2:
        # Host Down
        job = "host"
    elif len(source_parts) == 3:
        job = "service"
        service_name = source_parts[2]
    else:
        raise ValueError("invalid id")

    site = source_parts[0]
    host_name = source_parts[1]

    return job, site, host_name, service_name

def create_payload(data):
    """
    Create a String with URL Payloads to set ACK
    """
    payload = {
        '_ack_comment' : "Ticket: {}".format(data['QUELLEID']),
        '_secret' : app.config['CMK_SECRET'],
        '_username' : app.config["CMK_USER"],

    }

    job, site, host, svc = get_job(data)
    if job == "host":
        payload['view_name'] = 'hoststatus'
    elif job == "service":
        payload['service'] = svc
        payload['view_name'] = 'service_snow'
        #service down
    else:
        raise ValueError("invalid id")

    payload['site'] = site
    payload['host'] = host

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
                if data['host_in_downtime'] == 'yes' or data['svc_in_downtime'] == 'yes':
                    solved = True
                    # Now Fake a OK State of the Service in order to have a re notification
                    # in case the failure still exists after the Downtime (would not be notified
                    # if failure was before downtime started
                    url = "{url}check_mk/view.py?_fake_0=OK&_do_actions=yes&_fake_output=API+RESET"\
                    "&_do_confirm=yes&_transid=-1&{pl}".format(url=app.config['CMK_URL'],
                                                               pl=payload_str)
                    requests.get(url, verify=app.config['SSL_VERIFY'])
            else:
                if data['host_state'] != "UP" and data['host_in_downtime'] == 'no':
                    solved = False
                if data['host_in_downtime'] == 'yes':
                    solved = True
                    url = "{url}check_mk/view.py?_fake_0=UP&_do_actions=yes&_fake_output=API+RESET"\
                    "&_do_confirm=yes&_transid=-1&{pl}".format(url=app.config['CMK_URL'],
                                                               pl=payload_str)
                    requests.get(url, verify=app.config['SSL_VERIFY'])
        except JSONDecodeError:
            return {"status": str(response.text)}
        except (ValueError, IndexError) as msg:
            raise
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
            data = request.json
            job, site, host, svc = get_job(data)


            cmk_url = app.config['CMK_URL']
            payload = {
              "sticky": False,
              "persistent": False,
              "notify": False,
              "comment": f"Ticket : {data['QUELLEID']}",
              "host_name": host
            }
            if job == "host":
                url = f"{cmk_url}check_mk/api/1.0/domain-types/acknowledge/collections/host"
                payload['acknowledge_type'] = "host"
            elif job == "service":
                url = f"{cmk_url}check_mk/api/1.0/domain-types/acknowledge/collections/service"
                payload['acknowledge_type'] = "service"
                payload['service_description'] = svc

            username = app.config['CMK_USER']
            password = app.config['CMK_SECRET']
            headers = {
                'Authorization': f"Bearer {username} {password}"
            }
            response = requests.post(url, json=payload, verify=app.config['SSL_VERIFY'], headers=headers)
        except (ValueError, IndexError) as msg:
            return {"status" :str(msg)}, 500

        return {"status" : "success"}, 200
