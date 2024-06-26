""" /render
"""
import re

from flask import Blueprint
from flask import current_app as app
from flask import jsonify, request
from jinja2 import Environment, StrictUndefined, Undefined, meta
from ruamel.yaml import YAML

from td4a.models.exception_handler import ExceptionHandler, HandledException

api_render = Blueprint("api_render", __name__)


@ExceptionHandler
def jinja_unresolved(template, typ):
    """Check a jinja template for any unresolved vars"""
    _ = typ
    env = Environment()
    env.trim_blocks = True
    unresolved = meta.find_undeclared_variables(env.parse(template))
    return unresolved


def lookup(*args, **kwargs):  # pylint: disable=unused-argument
    return "unsupported"


@ExceptionHandler
def jinja_render(data, template, filters, typ):
    """Render a jinja template"""
    _ = typ
    if typ == "p1":
        env = Environment(undefined=Undefined)
    else:
        env = Environment(undefined=StrictUndefined)
    env.trim_blocks = True
    for entry in filters:
        env.filters[entry[0]] = entry[1]
    env.globals.update(lookup=lookup)
    result = env.from_string(template).render(data)
    return result


@ExceptionHandler
def yaml_parse(string, typ):
    """load yaml from string"""
    _ = typ
    yaml = YAML()
    yaml.load(string)


@ExceptionHandler
def render(payload, filters, typ):
    """Given the payload, render the result"""
    _ = typ
    try:
        loader = YAML(typ="unsafe")
        result = None
        if payload["p1"] and payload["p2"]:
            # check for error in data
            yaml_parse(string=payload["p1"], typ="p1")
            # swap '{{ }}' for "{{ }}"
            dq_jinja = re.compile(r"'\{\{([^\{\}]+)\}\}'")
            payload["p1"] = dq_jinja.sub('"{{\\1}}"', payload["p1"])
            # remove the quotes around dicts put into jinja
            expose_dicts = re.compile(r'"\{([^\{].*)\}"')
            # remove the quotes aournd lists put into jinja
            expose_lists1 = re.compile(r'"\[(.*)\]"')
            # change '{{ }}' to "{{ }}"
            dq_jinja = re.compile(r"'\{\{([^\{\}]+)\}\}'")

            raw_data = None
            after_jinja = payload["p1"]
            tvars = loader.load(payload["p1"])

            if jinja_unresolved(template=after_jinja, typ="p1"):
                while after_jinja != raw_data:
                    raw_data = after_jinja
                    after_jinja = jinja_render(
                        data=tvars,
                        template=raw_data,
                        filters=filters,
                        typ="p1")
                    yaml_ready = expose_dicts.sub("{\\1}", after_jinja)
                    yaml_ready = expose_lists1.sub("[\\1]", yaml_ready)
                    yaml_ready = dq_jinja.sub('"{{\\1}}"', yaml_ready)
                    tvars = loader.load(yaml_ready)
            result = jinja_render(
                data=tvars,
                template=payload['p2'],
                filters=filters,
                typ="p2")
        return {"p3": result}
    except HandledException as error:
        return error.json()


@api_render.route("/render", methods=["POST"])
def rest_render():
    """render path"""
    try:
        app.logger.info("Checking and parsing data...")
        if app.args.log_level == "DEBUG":
            app.logger.debug("Input data:\n%s", request.json.get("p1"))
            app.logger.debug("Template data:\n%s", request.json.get("p2"))

        response = render(
            payload=request.json,
            filters=app.filters,
            typ="page")

        if response.get("handled_error"):
            raise HandledException({"json": response})

        app.logger.info("Rendered response.")
        if app.args.log_level == "DEBUG":
            app.logger.debug("Output data:\n%s", response.get("p3"))
        return jsonify(response)
    except HandledException as error:
        app.logger.error(error.json())
        return jsonify(error.json())
