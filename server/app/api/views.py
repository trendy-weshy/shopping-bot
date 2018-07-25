from . import api
import datetime
from flask import jsonify
from flask_cors import cross_origin


@api.after_request
def apply_caching(response):
    response.headers["Content-type"] = "application/json"
    return response


@api.route("/ping")
@cross_origin()
def ping_api():
    return jsonify(time=datetime.datetime.now())

