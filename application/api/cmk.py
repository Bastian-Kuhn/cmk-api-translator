"""
Enpoints
"""
# pylint: disable=function-redefined
# pylint: disable=no-self-use
# pylint: disable=no-member
# pylint: disable=too-few-public-methods
from flask import request
from flask_restplus import Namespace, Resource, fields

API = Namespace('cmk')


ACK_DATA = API.model('acknowledgment', {
    "QUELLE" : fields.String,
    "QUELLEID": fields.String,
    "ZIEL" : fields.String,
    "ZIELID" : fields.String,
})


@API.route('ack/')
class AckApi(Resource):
    """
    Acknowledgement API
    """

    @API.expect(ACK_DATA, validate=True)
    def post(self):
        """
        Create a new subscription
        """
        data = request.json
        return str(data), 200
