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
from pyangbind.lib.yangtypes import RestrictedPrecisionDecimalType, RestrictedClassType, TypedListType
from pyangbind.lib.yangtypes import YANGBool, YANGListType, YANGDynClass, ReferenceType
from pyangbind.lib.base import PybindBase
from resource.datastore import dataStore
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

generated_dir = GENERATED_DIR_NAME  # Generated subdirectory name
models = []  # List of YANG modes we dynamically imported


def _get_extmethods(element, path_base='', extmethods=None):
    """
    A recursive function to convert a yang model into a extmethods dictionary

    :param element: (list of YANGDynClass) Child elements of a the model instance
    :param path_base: (dict) Existing dictionary of elements
    :param extmethods: (dict) Existing dictionary of elements

    :return: (dict) A Pyangbind compatible extmethods dictionary
    """
    extmethods = extmethods if extmethods is not None else {}

    if element is None:
        return extmethods

    if isinstance(element, dict):
        print '%s is a dictionary of length %d' % (element, len(element))

        for key, value in element.items():
            path = path_base + '/' + key
            config = False  # TODO Not really what we want
            extmethods[path] = config
            return _get_extmethods(value, path_base=path, extmethods=extmethods)

    elif isinstance(element, PybindBase):
        print '  is config: %s' % 'True' if element._is_config else 'False'
        print '     is key: %s' % 'True' if element._is_keyval else 'False'
        print ' is default: %s' % 'True' if element.default() else 'False'
        print 'has changed: %s' % 'True' if element._changed() else 'False'
        return extmethods

    # elif isinstance(value, list) or isinstance(value, tuple):
    #     for v in value:
    #         for d in _get_extmethods(v,
    #                                  path_base=path_base + '%s/' % key,
    #                                  extmethods=extmethods):
    #             return d
    else:
        return extmethods
        #
        #
        # if type(element) is YANGDynClass:
        #     print 'It is the base YANG type'
        #     yield extmethods


def _import_models():
    """
    Import the models in the generated directory.

    The 'generated' directory is expected to be a subdirectory the directory that
    contains this file. It typically is a symbolic link over to the 'modules'
    generated-code subdirectory.
    """
    gen_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), generated_dir)

    if os.path.exists(gen_dir) and os.path.isdir(gen_dir):
        if args.verbose > 0:
            print 'The generatedDir is %s' % gen_dir

        # Walk all the files in the generated code directory and look for python files

        files = [f for f in os.listdir(gen_dir)
                 if os.path.isfile(os.path.join(gen_dir, f)) and
                 f.split('.')[-1].lower() == 'py' and
                 f != '__init__.py'
                 ]

        if args.verbose > 0:
            print 'The list of python files in the generated directory is: %s' % files

        for filename in files:
            # The class name for the model is the same as the first part of the filename

            model = str.split(filename, '.')[0]
            if args.verbose > 0:
                print "Found model '%s' in '%s'" % (model, filename)
            package = generated_dir
            module = model
            _class = model

            try:
                # yang_model = dynamic_import(package, _class)

                if args.verbose > 0:
                    print 'Dynamic import -> from %s.%s import %s' % (package, module, _class)

                yang_module = __import__('%s.%s' % (package, module), fromlist=[_class])
                yang_model = getattr(yang_module, _class)

                if args.verbose > 0:
                    print 'Yang class imported: %s' % yang_model

                # Create an instance of this yang model.  This will be an YANG Container object
                # that derives from the PybindBase.  We want to walk it and extract the paths
                # for all configuration nodes and return a dictionary compatible with pyangbind
                # extmethod

                extmethods = _get_extmethods(yang_model().elements())
                pprint.PrettyPrinter(indent=4).pprint(extmethods)

                # Get a dictionary of the top level container. Do not filter out any children

                container_dict = yang_model().get()
                pprint.PrettyPrinter(indent=4).pprint(container_dict)

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
    _import_models()

    if args.verbose > 0:
        print 'Starting up web server on port %d' % args.http_port

    app.run(debug=True, port=args.http_port)
