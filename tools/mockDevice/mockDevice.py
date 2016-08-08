#!/usr/bin/python
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
from flask import Flask, Response
from werkzeug.routing import BaseConverter
from xrd import Element, XRD, Link
from globals import DEFAULT_ROOT_RESOURCE, DEFAULT_HTTP_PORT, GENERATED_DIR_NAME
from resource.datastore import dataStore

# import pprint

try:
    from generated import *
except ImportError:
    print 'Did not find generated code subdirectory with any YANG models'

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
parser.add_argument('--disable_schema', '-s', action='store_true', default=False,
                    help='Disable support for RESTCONF optional schema resource')
parser.add_argument('--default_xml', '-x', action='store_true', default=False,
                    help='Specifies that XML encoding is the default if not specified otherwise '
                         'by the clients "Accept" header, default is JSON')
parser.add_argument('--accept_patch', '-P', action='store_true', default=False,
                    help='Specifies that the PATCH method is supported, default is False')

args = parser.parse_args()

app = Flask(__name__)
__prefix = '/%s/data' % args.root_resource
app.register_blueprint(dataStore, url_prefix=__prefix)

###########################################################################

_generated_dir = GENERATED_DIR_NAME  # Generated subdirectory name

# RESTCONF API Resources

operations = None  # TODO Not yet implemented
notifications = None  # TODO Not yet implemented

# Some other args that dependent models need access to
default_json = not args.default_xml
accept_patch = args.accept_patch


def default_encoding_json():
    """
    :returns: (boolean) Flag indicating, if true, the default content encoded is JSON
    """
    global default_json
    return default_json


def default_encoding_xml():
    """
    :returns: (boolean) Flag indicating, if true, the default content encoded is XML
    """
    return not default_encoding_json()


def accept_patch():
    """
    :returns: (boolean) Flag indicating, if true, that the PATCH command is supported
    """
    return accept_patch


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


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


class WildcardConverter(BaseConverter):
    #
    # Match empty OR slash followed by zero or more characters

    regex = r'(|/.*?)'
    weight = 200


if __name__ == '__main__':
    from dataModels import register_data_models
    from yangLibrary import register_yang_library_version
    from apiResource import register_top_level_resource

    # Our URLs can get complex

    app.url_map.converters['regex'] = RegexConverter
    app.url_map.converters['wildcard'] = WildcardConverter

    # Import and register any data models found in the generated subdirectory

    register_data_models(_generated_dir, args.root_resource, verbose=args.verbose)

    # The yang library version needs to be created/registered after any data models are imported

    if not args.disable_schema:
        register_yang_library_version(args.root_resource, verbose=args.verbose)

    # Create/register the top level API resource last since it is dependent on all its
    # children being in place

    register_top_level_resource(args.root_resource, verbose=args.verbose)

    if args.verbose > 0:
        print 'Starting up web server on port %d' % args.http_port

    app.run(debug=True, port=args.http_port)
