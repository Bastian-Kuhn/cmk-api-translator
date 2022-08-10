"""
API Endpoints
"""
from flask import Blueprint
from flask_restplus import Api

from .cmk import API as cmk
from .cmk2 import API as cmk2
from .graylog33 import API as graylog33

API_BP = Blueprint('api', __name__)

API = Api(API_BP)

API.add_namespace(cmk, path='/')
API.add_namespace(cmk2, path='/cmk2')
API.add_namespace(graylog33, path='/graylog/v3.3')
