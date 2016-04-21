#
# Copyright 2015 - 2016 Boling Consulting Solutions, bcsw.net
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
from flask import Response, request
from mockDevice import app, operations
from dataModels import data_models
from yangLibrary import yang_library

from globals import DEFAULT_ROOT_RESOURCE, DEFAULT_HTTP_PORT, GENERATED_DIR_NAME
from resource.datastore import dataStore
from yangModel import YangModel
from yangLibrary import YangLibrary, yang_library


def register_top_level_resource(root_resource, verbose=False):
    """
    Retrieve the Top-level API Resource
    """
    # Register with flask
    app.add_url_rule(root_resource, view_func=_top_level_api_get, methods=['GET'])


def _top_level_api_get():
    # Look at the Accept header.  Expect one of the following two
    #  application/yang.data+xml (default)
    #  application/yang.data+json
    allowed = ['application/yang.data+xml', 'application/yang.data+json']
    accepted = request.headers.get('Accept', 'application/yang.data+xml')

    if accepted not in allowed:
        pass  # TODO

    result = {}

    if data_models is not None:
        result['data'] = {}  # TODO go further

    if operations is not None:
        result['operations'] = {}  # TODO go further

    # Schema Resource is optional
    if yang_library is not None:
        result['yang-library-version'] = {}  # TODO go further

    # TODO Notifications?
    pass
