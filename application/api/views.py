"""
API Endpoints
"""
from flask import Blueprint
from flask_restplus import Api

from .cmk import API as cmk

API_BP = Blueprint('api', __name__)

API = Api(API_BP)

API.add_namespace(cmk, path='/')
