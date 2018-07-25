from manage import application as app
from flask import jsonify


@app.app_errorhandler(400)
def bad_request(e):
    return jsonify(error='Bad requests'), 400


@app.app_errorhandler(401)
def unauthorized(e):
    return jsonify(error='Unauthorized'), 401


@app.app_errorhandler(403)
def unauthenticated(e):
    return jsonify(error='Unauthenticated Access'), 403


@app.app_errorhandler(404)
def not_found(e):
    return jsonify(error='Not found'), 404\
    

@app.app_errorhandler(405)
def not_allowed(e):
    return jsonify(error='Not allowed'), 405


@app.app_errorhandler(500)
def server_error(e):
    return jsonify(error='Server error'), 500