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
from datetime import datetime
from uuid import uuid4

data_models = []  # List of YANG models we dynamically imported
_path_to_model = {}  # Dictionary of base directory to YANG model

# Maintain a last-modified timestamp and eTag for the entire datastore
# resource

datastore_lastModifiedTimestamp = datetime.utcnow()
datastore_eTag = str(uuid4())


def update_datastore(ts, tag):
    global datastore_lastModifiedTimestamp
    global datastore_eTag
    datastore_lastModifiedTimestamp = ts
    datastore_eTag = tag


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

    data_url_regex = '/%s/data<regex():path>' % root_resource

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

    The "api-path" Augmented Backus-Naur Form (ABNF) syntax is used to
    construct RESTCONF path identifiers:

     api-path = '/' |
                ('/' api-identifier
                0 * ('/' (api-identifier | list-instance )))

    api-identifier = [module-name ":"] identifier      ;; note 1

    module-name = identifier

    list-instance = api-identifier '=' key-value [',' key-value]*

    key-value = string       ;; note 1

    string = <a quoted or unquoted string>

        # An identifier MUST NOT start with
        # (('X'|'x) ('M'|'m') ('L'|'l'))

    identifier = (ALPHA / '_')
                 *(ALPHA / DIGIT / '_' / '-' / '.')

    Note 1: The syntax for "api-identifier" and "key-value" MUST conform
    to the JSON identifier encoding rules in Section 4 of
    [I-D.ietf-netmod-yang-json].

    A RESTCONF data resource identifier is not an XPath expression. It
    is encoded from left to right, starting with the top-level data node,
    according to the "api-path" rule in Section 3.5.1.1. The node name
    of each ancestor of the target resource node is encoded in order,
    ending with the node name for the target resource. If a node in the
    path is defined in another module than its parent node, then module
    name followed by a colon character (":") is prepended to the node
    name in the resource identifier. See Section 3.5.1.1 for details.

    If a data node in the path expression is a YANG leaf-list node, then
    the leaf-list value MUST be encoded according to the following rules:

    o The instance-identifier for the leaf-list MUST be encoded using
      one path segment [RFC3986].

    o The path segment is constructed by having the leaf-list name,
      followed by an "=" character, followed by the leaf-list value.
      (e.g., /restconf/data/top-leaflist=fred).

    If a data node in the path expression is a YANG list node, then the
    key values for the list (if any) MUST be encoded according to the
    following rules:

    o The key leaf values for a data resource representing a YANG list
      MUST be encoded using one path segment [RFC3986].

    o If there is only one key leaf value, the path segment is
      constructed by having the list name, followed by an "=" character,
      followed by the single key leaf value.

    o If there are multiple key leaf values, the path segment is
      constructed by having the list name, followed by the value of each
      leaf identified in the "key" statement, encoded in the order
      specified in the YANG "key" statement. Each key leaf value except
      the last one is followed by a comma character.

    o The key value is specified as a string, using the canonical
      representation for the YANG data type. Any reserved characters
      MUST be percent-encoded, according to [RFC3986], section 2.1.

    o All the components in the "key" statement MUST be encoded.
      Partial instance identifiers are not supported.

    o Since missing key values are not allowed, two consecutive commas
      are interpreted as a zero-length string. (example:
      list=foo,,baz).

    o The "list-instance" ABNF rule defined in Section 3.5.1.1
      represents the syntax of a list instance identifier.

    o Resource URI values returned in Location headers for data
      resources MUST identify the module name, even if there are no
      conflicting local names when the resource is created. This
      ensures the correct resource will be identified even if the server
      loads a new module that the old client does not know about.

    :param path: The url path following the 'data' in the url.
    """
    # Look at the Accept header.  Expect one of the following two
    #  application/yang.data+xml (default)
    #  application/yang.data+json
    allowed = ['application/yang.data+xml', 'application/yang.data+json']
    accepted = request.headers.get('Accept', 'application/yang.data+xml')
    return
    pass
