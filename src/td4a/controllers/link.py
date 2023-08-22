import requests
from flask import Blueprint
from flask import current_app as app
from flask import jsonify, request

from td4a.models.exception_handler import ExceptionHandler, HandledException

api_link = Blueprint("api_link", __name__)


@ExceptionHandler
def link(payload, args, typ):
    """store a doc in the db"""
    _ = typ
    auth = (args.username, args.password)
    url = args.url
    response = requests.post(url, json=payload, auth=auth, timeout=5)
    return {"id": response.json()["id"]}


@api_link.route("/link", methods=["POST"])
def rest_link():
    """Save the documents in a couchdb and returns an id"""
    try:
        response = link(payload=request.json, args=app.args, typ="link")
        return jsonify(response)
    except HandledException as error:
        return jsonify(error.json())
