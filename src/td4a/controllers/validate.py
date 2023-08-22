""" /retrieve
"""
from flask import Blueprint, jsonify, request
from jsonschema import Draft4Validator, FormatChecker
from jsonschema.exceptions import UnknownType

from td4a.models.exception_handler import ExceptionHandler, HandledException
from td4a.models.td4ayaml import Td4aYaml

api_validate = Blueprint('api_validate', __name__)


@ExceptionHandler
def parse_yaml(yamul, typ):
    _ = typ
    yaml = Td4aYaml()
    obj = yaml.load(yamul)
    return obj


def validation(payload):
    """ Validate schema from data
    """
    try:
        yaml_safe = Td4aYaml(typ='safe')
        yaml = Td4aYaml()
        data = yaml_safe.load(payload['p1'])
        schema = yaml_safe.load(payload['p2'])
        errors = []
        validator = Draft4Validator(schema, format_checker=FormatChecker())
        for error in sorted(validator.iter_errors(data)):
            errors.append(error.message)
        if errors:
            return {"p3": yaml.dump({"messages": errors})}
        return {"p3": yaml.dump({"messages": ["validation passed"]})}
    except UnknownType as error:
        error_message = str(error)
        lines = error_message.splitlines()
        message = [x for x in lines if x.startswith('Unknown type')]
        return {"p3": yaml.dump({"messages": message})}


@api_validate.route('/validate', methods=['POST'])
def rest_validate():
    """ Build a schema for data
    """
    try:
        payload = request.json
        response = validation(payload=payload)
        return jsonify(response)
    except HandledException as error:
        return jsonify(error.json())
