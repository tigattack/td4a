""" /inventory
"""
import json

from flask import Blueprint
from flask import current_app as app
from flask import jsonify, request

from td4a.models.td4ayaml import Td4aYaml

api_inventory = Blueprint("api_inventory", __name__)


@api_inventory.route("/inventory", methods=["GET"])
def rest_inventory():
    """return inventory for host"""
    yaml = Td4aYaml()
    inventory = app.inventory.get(request.args.get("host"), "")
    data = json.loads(json.dumps(inventory))
    response_text = ""
    for section in sorted(data.keys()):
        response_text += yaml.dump({section: data[section]})
    response = {"p1": response_text}
    return jsonify(response)
