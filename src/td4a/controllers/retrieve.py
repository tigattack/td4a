""" /retrieve
"""
import requests
from flask import Blueprint
from flask import current_app as app
from flask import jsonify, request

from td4a.models.exception_handler import ExceptionHandler, HandledException

api_retrieve = Blueprint("api_retrieve", __name__)


@ExceptionHandler
def retrieve(doc_id, typ):
    """get a doc from the db"""
    _ = typ
    auth = (app.args.username, app.args.password)
    url = app.args.url
    cdoc = requests.get(
        f"{url}/{doc_id}?include_docs=true",
        auth=auth,
        timeout=5)
    doc = cdoc.json()
    if cdoc.status_code == 200:
        response = {"panels": doc["panels"], "config": doc["config"]}
    else:
        response = {
            "handled_error": {
                "in": "document retrieval",
                "title": "Message: Issue loading saved document.",
                "line_number": None,
                "details": f"Details: {doc['error']}",
                "raw_error": f"{cdoc.text}",
            }
        }
    return response


@api_retrieve.route("/retrieve", methods=["GET"])
def rest_retrieve():
    """return a doc from the couchdb"""
    try:
        response = retrieve(doc_id=request.args.get("id"), typ="link")
        return jsonify(response)
    except HandledException as error:
        return jsonify(error.json())
