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

generated_dir = GENERATED_DIR_NAME  # Generated subdirectory name
models = []  # List of YANG modes we dynamically imported


def dynamic_import(_package, _class):
    """
    Dynamically import a class based on a variable

    :param _package: (string) The package prefix(es)
    :param _class: (string) The class name you are looking for

    :return:  The module to import
    """
    full_path = _package + '.' + _class
    components = full_path.split('.')
    module = __import__(components[0])
    for component in components[1:]:
        module = getattr(module, component)
    return module


def import_models():
    """
    Import the models in the generated directory.

    The 'generated' directory is expected to be a subdirectory the directory that
    contains this file. It typically is a symbolic link over to the 'modules'
    generated-code subdirectory.
    """
    gen_dir = os.path.join(os.path.realpath(__file__), generated_dir)

    if os.path.exists(gen_dir) and os.path.isdir(gen_dir):
        print 'The generatedDir is %s' % gen_dir

        # Walk all the files in the generated code directory and look for python files

        files = [f for f in os.listdir(gen_dir) if os.isfile(os.path.join(gen_dir, f))]
        for filename in files:
            file_parts = os.path.splitext(v)
            if file_parts[1].lower() is '.py':

                # The class name for the model is the same as the first part of the filename

                model = file[0]
                print "Found model '%s' in '%s'" % (model, filename)
                package = generated_dir
                module = model
                _class = model

                try:
                    # yang_model = dynamic_import(package, _class)
                    yang_module = __import__('%s.%s' % (package, module), fromlist=[_class])
                    yang_model = getattr(yang_module, _class)

                    #      TODO: Implement the rest of this
                    # Basically we want to walk the model and for each 'config' element, we want
                    # to set up an extension that makes use of the restconfConfigHelper class.
                    # We then add this

                except ImportError:
                    print 'Import Error while attempting to import class %s from %s.%s' % (model, package, module)

                    # Instantiate the models the first time so we can generate all the paths within
                    # them so we can create extension methods that provide for RESTCONF required
                    # methods
                    ###########################################################################


@app.route('/')
def index():
    return "This is a test program to simulate a RESTCONF capable device.<br\>"


@app.route('/.well-known/host-meta', methods=['GET'])
def get_host_meta():
    """
    This function services the well-known host-meta XRD data for RESTCONF
    API root discovery.
    """
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
    pass  # TODO: Need to implement


if __name__ == '__main__':
    import_models()
    app.run(debug=True, port=args.http_port)
