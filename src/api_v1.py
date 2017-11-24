from flask import Blueprint, request, Response
#  from flask.json import jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
from difflib import SequenceMatcher
import json
from .generate_manifest import PomXMLTemplate
from .exceptions import HTTPError

app_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')
rest_api = Api(app_v1)
CORS(app_v1)
_resource_paths = list()

json_response = json.load(open('src/response.json'))


def add_resource_no_matter_slashes(resource, route,
                                   endpoint=None, defaults=None):
    slashless = route.rstrip('/')
    _resource_paths.append(app_v1.url_prefix + slashless)
    slashful = route + '/'
    endpoint = endpoint or resource.__name__.lower()
    defaults = defaults or {}

    rest_api.add_resource(resource,
                          slashless,
                          endpoint=endpoint + '__slashless',
                          defaults=defaults)
    rest_api.add_resource(resource,
                          slashful,
                          endpoint=endpoint + '__slashful',
                          defaults=defaults)


class ApiEndpoints(Resource):
    def get(self):
        return {'paths': sorted(_resource_paths)}


def validation_checker(packages):
    # TODO Implementation of validation checker
    # currently returning mock response
    packages = sorted(packages.get('packages'))
    comp_package = packages[0]
    _response = {pkg: 'valid'
                 if SequenceMatcher(None, comp_package, pkg).ratio() > 0.4 else 'invalid'
                 for pkg in packages}
    return _response


class UserIntent(Resource):

    @staticmethod
    def post():
        input_string = request.get_json()

        if not input_string:
            raise HTTPError(400, error="Expected String in request")
    # TODO Implementation of user intent logic
    # currently returning mock response
        return json_response.get('userIntent')


class PackageRecommendation(Resource):

    @staticmethod
    def get(tag):
        if not tag:
            raise HTTPError(400, error="Expected tag in request")
    # TODO Implementation of package Recommendation logic
    # currently returning mock response
        return json_response.get('packageRecommendation')


class DependencyValidation(Resource):

    @staticmethod
    def post():
        input_json = request.get_json()

        if not input_json:
            raise HTTPError(400, error="Expected String in request")

        if 'ecosystem' not in input_json:
            raise HTTPError(400, "Must provide an ecosystem")

        if 'packages' not in input_json:
            raise HTTPError(400, error="Expected packages in the request")

        _response = validation_checker(input_json)
        if all([v == 'valid' for k, v in _response.items()]):
            if input_json.get('ecosystem') == 'maven':
                return Response(
                    PomXMLTemplate(input_json).xml_string(),
                    headers={
                        "Content-disposition": 'attachment;filename=pom.xml',
                        "Content-Type": "text/xml;charset=utf-8"
                    }
                )
            else:
                return Response(
                    {'result': "ecosystem '{}' is not yet supported".format(
                        input_json['ecosystem'])},
                    status=400
                )
        else:
            return _response


add_resource_no_matter_slashes(ApiEndpoints, '')
add_resource_no_matter_slashes(UserIntent, '/user-intent')
add_resource_no_matter_slashes(
    PackageRecommendation, '/package-recommendation/<tag>')
add_resource_no_matter_slashes(DependencyValidation, '/dependency-validation')
