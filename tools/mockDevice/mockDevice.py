#!/usr/bin/python
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
from flask import Flask, Response
from xrd import Element, XRD, Link
from globals import DEFAULT_ROOT_RESOURCE, DEFAULT_HTTP_PORT, GENERATED_DIR_NAME
from resource.datastore import dataStore
from yangModel import YangModel
import pprint

try:
    from generated import *
except ImportError:
    print 'Did not find generated code subdirectory with any YANG models'

import os
import argparse

###########################################################################
# Parse the command line

parser = argparse.ArgumentParser(description='Mock RESTCONF Device')
parser.add_argument('--verbose', '-v', action='store_true', default=False,
                    help='Output verbose information')
parser.add_argument('--root_resource', '-r', action='store', default=DEFAULT_ROOT_RESOURCE,
                    help='RESTCONF Root Resource')
parser.add_argument('--http_port', '-p', action='store', default=DEFAULT_HTTP_PORT,
                    help='HTTP Port number')

args = parser.parse_args()

app = Flask(__name__)
__prefix = '/%s/data' % args.root_resource
app.register_blueprint(dataStore, url_prefix=__prefix)

###########################################################################

_generated_dir = GENERATED_DIR_NAME  # Generated subdirectory name


def _import_models():
    """
    Import the models in the generated directory.

    The 'generated' directory is expected to be a subdirectory the directory that
    contains this file. It typically is a symbolic link over to the 'modules'
    generated-code subdirectory.

    :returns: (list of YangModel) List of imported YANG Models
    """
    models = []  # List of YANG models we dynamically imported

    gen_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), _generated_dir)

    if os.path.exists(gen_dir) and os.path.isdir(gen_dir):
        if args.verbose > 0:
            print 'The generatedDir is %s' % gen_dir

        # Walk all the files in the generated code directory and look for YIN XM files
        # and use that to determine the python code-generated names

        xml_files = [f for f in os.listdir(gen_dir)
                     if os.path.isfile(os.path.join(gen_dir, f)) and
                     f.split('.')[-1].lower() == 'xml'
                     ]

        if args.verbose > 0:
            print 'The list of XML files in the generated directory is: %s' % xml_files

        for filename in xml_files:
            # The class name for the model is the same as the first part of the filename

            model = YangModel(gen_dir, filename, _generated_dir, verbose=args.verbose)

            if args.verbose > 0:
                print "Found model '%s' in '%s'" % (model.name, filename)

            models.append(model)

    if args.verbose:
        print('_import_models found %d YANG models', len(models))

    return models


def _register_models(models):
    """
    Register any imported YANG modes with flask

    :param models: (list of YangModel) Imported YANG models
    """

    data_dir = args.root_resource + '/data'

    for model in models:
        if args.verbose:
            print('Registering YANG models %s with flask', model.name)

        # for container in mode.
        container = 'test'
        model_dir = '%s/%s:%s' % (data_dir, model.name, container)

        pass  # TODO: Need to implement

        # app.add_url_rule
        #
        #     Basically this example::
        #
        #     @app.route('/')
        #     def index():
        #         pass
        #
        # Is equivalent to the following::
        #
        # def index():
        #     pass
        # app.add_url_rule('/', 'index', index)
        #
        # :param rule: the URL rule as string
        # :param endpoint: the endpoint for the registered URL rule.  Flask
        #                   itself assumes the name of the view function as
        #                   endpoint
        # :param view_func: the function to call when serving a request to the
        #                   provided endpoint
        # :param options: the options to be forwarded to the underlying
        # :class:`~werkzeug.routing.Rule` object.  A change
        # to Werkzeug is handling of method options.  methods
        # is a list of methods this rule should be limited
        # to (`GET`, `POST` etc.).  By default a rule
        # just listens for `GET` (and implicitly `HEAD`).
        # Starting with Flask 0.6, `OPTIONS` is implicitly
        # added and handled by the standard request handling.


def _yang_library_get():
    # Look at the Accept header.  Expect one of the following two
    #  application/yang.data+xml
    #  application/yang.data+json

    pass


def _register_yang_library_version():
    """
    This mandatory leaf identifies the revision date of the
    "ietf-yang-library" YANG module that is implemented by this server.
    """
    lib_dir = args.root_resource + '/yang-library-version'
    app.add_url_rule(lib_dir, view_func=_yang_library_get, methods=['GET'])


@app.route('/')
def index():
    return "This is a test program to simulate a RESTCONF capable device.<br\>"


@app.route('/.well-known/host-meta', methods=['GET'])
def get_host_meta():
    """
    This function services the well-known host-meta XRD data for RESTCONF
    API root discovery.
    """
    if args.verbose > 0:
        print 'get_host_meta: entry'

    xrd_obj = XRD()

    # Add a few extra elements and links before RESTCONF to help make sure
    # the parsing/XPATH is correct

    xrd_obj.elements.append(Element('hm:Host', 'testDevice'))
    xrd_obj.links.append(Link(rel='license', href='http://www.apache.org/licenses/LICENSE-2.0'))
    xrd_obj.links.append(Link(rel='author', href='http://bcsw.net'))

    # Add the link for RESTCONF

    xrd_obj.links.append(Link(rel='restconf', href=args.root_resource))

    # Add some extra links here as well

    xrd_obj.links.append(Link(rel='testPath', href='this/does/not/exist'))
    xrd_obj.links.append(Link(rel='http://oexchange.org/spec/0.8/rel/resident-target',
                              type_='application/xrd+xml',
                              href='http://twitter.com/oexchange.xrd'))

    # Convert to XML, pretty-print it to aid in debugging

    xrd_doc = xrd_obj.to_xml()

    return Response(xrd_doc.toprettyxml(indent=' '), mimetype='application/xrd+xml')


@app.route('/config/reset', methods=['POST'])
def do_reset():
    """
    This url (/config/reset) can be called to reset configurable parameters
    to their defaults.

    This allows you to run the server once and call various 'config/set/*' pages
    with variables to alter the behaviour (for a particular test) and then call
    this to reset items back to normal so you can do more tests.
    """
    if args.verbose > 0:
        print 'TODO: Need to implement configuration reset capability'

    return

if __name__ == '__main__':

    # Import any models found in the generated subdirectory

    _register_models(_import_models())
    _register_yang_library_version()

    if args.verbose > 0:
        print 'Starting up web server on port %d' % args.http_port

    app.run(debug=True, port=args.http_port)
