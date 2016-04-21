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
from yangModel import YangModel
import os
from mockDevice import app

data_models = []  # List of YANG models we dynamically imported
_path_to_model = {}  # Dictionary of base directory to YANG model


def _import_data_models(model_dir, verbose=False):
    """
    Import the data (config/non-config) models in the generated directory.

    The 'generated' directory is expected to be a subdirectory the directory that
    contains this file. It typically is a symbolic link over to the 'modules'
    generated-code subdirectory.

    :param model_dir: (string) Directory containing code-generated models
    :param verbose: (int) Enables verbose output
    """
    gen_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), model_dir)

    if os.path.exists(gen_dir) and os.path.isdir(gen_dir):
        if verbose > 0:
            print 'The base code-gen directory is %s' % gen_dir

        # Walk all the files in the generated code directory and look for YIN XM files
        # and use that to determine the python code-generated names

        xml_files = [f for f in os.listdir(gen_dir)
                     if os.path.isfile(os.path.join(gen_dir, f)) and
                     f.split('.')[-1].lower() == 'xml'
                     ]

        if verbose > 0:
            print 'The list of XML files in the generated directory is: %s' % xml_files

        for filename in xml_files:
            # The class name for the model is the same as the first part of the filename

            model = YangModel(gen_dir, filename, model_dir, verbose=verbose)

            if verbose > 0:
                print "Found model '%s' in '%s'" % (model.name, filename)

            data_models.append(model)

    if verbose:
        print('_import_models found %d YANG models', len(data_models))


def register_data_models(model_dir, root_resource, verbose=False):
    """
    Register any imported YANG modes with flask

    :param model_dir: (string) Directory containing code-generated models
    :param root_resource: (string) Base API resource.  Ie  'restconf', 'top/restconf', ...
    :param verbose: (int) Enables verbose output
    """
    # Import them first

    _import_data_models(model_dir, verbose=False)

    # Now register a base URL to catch them all
    # TODO: Work with the regular expression custom converter and see if we can get it to do better parsing

    data_base = '/%s/data' % root_resource
    data_url = '/%s/data<wildcard:path>' % root_resource
    app.add_url_rule(data_url, view_func=_data_get, methods=['GET'])

    for model in data_models:
        if verbose:
            print '[%s] Registering YANG model path' % model.name

        model_dir = '%s/%s' % (data_base, model.name)
        _path_to_model[model_dir] = model


def _data_get(path):
    """
    Perform a GET operation on {+restconf}/data...

    The 'path' parameter is provided to us by a custom converter that allows us to trap items
    after the 'path' in the URL above.  For instance the following that are not marked '404 NOT FOUND'
    below should be passed to us.

    .../data                         -> path = ''
    .../data/                        -> path = '/'
    .../data/toaster                 -> path = '/toaster'
    .../data/example-jukebox:jukebox -> path = '/example-jukebox:jukebox'
    .../datastuff                    -> 404 NOT FOUND

    :param path: The url path following the 'data' in the url.
    """
    # Look at the Accept header.  Expect one of the following two
    #  application/yang.data+xml (default)
    #  application/yang.data+json
    allowed = ['application/yang.data+xml', 'application/yang.data+json']
    accepted = request.headers.get('Accept', 'application/yang.data+xml')
    return
    pass
