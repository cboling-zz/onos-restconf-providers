#
# Copyright 2015-present Boling Consulting Solutions, bcsw.net
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
from ietf_yang_library import ietf_yang_library
from mockDevice import app
from dataModels import data_models

yang_library = None


def register_yang_library_version(root_resource, verbose=False):
    """
    This mandatory leaf identifies the revision date of the
    "ietf-yang-library" YANG module that is implemented by this server.

    :param root_resource: TODO: Comment this
    :param verbose: (int) Enables verbose output
    """
    yang_ibrary = YangLibrary(data_models)

    for model in data_models:
        pass

    # TODO The IETF YANG Library modules supports notifications.  Do we want to support this?

    # Register with flask

    lib_dir = '/%s/yang-library-version:modules' % root_resource
    app.add_url_rule(lib_dir, view_func=_yang_library_get, methods=['GET'])


def _yang_library_get():
    # Look at the Accept header.  Expect one of the following two
    #  application/yang.data+xml
    #  application/yang.data+json
    allowed = ['application/yang.data+xml', 'application/yang.data+json']
    accepted = request.headers.get('Accept', 'application/yang.data+xml')
    return
    pass


class YangLibrary(object):
    """
    Class that provides the contents of the {+restconf}/yang-library-version
    """

    def __init__(self, models):
        self.lib_class = ietf_yang_library()
        self._models = models
        pass
