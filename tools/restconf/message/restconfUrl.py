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
from urlparse import urlparse


class RestconfUrl(object):
    """
    URL Parse wrapper for RESTCONF

    This class is responsible for validating RESTCONF URL syntax according to
    draft-10 rules


    5.1. Request URI Structure

    Resources are represented with URIs following the structure for
    generic URIs in [RFC3986].

    A RESTCONF operation is derived from the HTTP method and the request
    URI, using the following conceptual fields:

        <OP> /<restconf>/<path>?<query>#<fragment>
         ^        ^         ^      ^        ^
         |        |         |      |        |
       method   entry   resource query   fragment
          M      M         O       O        I

        M=mandatory, O=optional, I=ignored

        where:

            <OP> is the HTTP method

            <restconf> is the RESTCONF entry point

            <path> is the Target Resource URI

            <query> is the query parameter list

            <fragment> is not used in RESTCONF

    =====================================================================

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

    =================================================================
    And if that is not enough, here is more from section 5.1 of draft 10

    5.1. Request URI Structure

    Resources are represented with URIs following the structure for
    generic URIs in [RFC3986].

    A RESTCONF operation is derived from the HTTP method and the request
    URI, using the following conceptual fields:

        <OP> /<restconf>/<path>?<query>#<fragment>
         ^        ^         ^      ^        ^
         |        |         |      |        |
       method   entry   resource query   fragment
         M        M        O       O        I

        M=mandatory, O=optional, I=ignored

        where:

            <OP> is the HTTP method

            <restconf> is the RESTCONF entry point

            <path> is the Target Resource URI

            <query> is the query parameter list

            <fragment> is not used in RESTCONF

    o method: the HTTP method identifying the RESTCONF operation
      requested by the client, to act upon the target resource specified
      in the request URI. RESTCONF operation details are described in
      Section 4.

    o entry: the root of the RESTCONF API configured on this HTTP
      server, discovered by getting the "/.well-known/host-meta"
      resource, as described in Section 3.1.

    o resource: the path expression identifying the resource that is
      being accessed by the operation. If this field is not present,
      then the target resource is the API itself, represented by the
      media type "application/yang.api".

    o query: the set of parameters associated with the RESTCONF message.
      These have the familiar form of "name=value" pairs. Most query
      parameters are optional to implement by the server and optional to
      use by the client. Each optional query parameter is identified by
      a URI. The server MUST list the optional query parameter URIs it
      supports in the "capabilities" list defined in Section 9.3.

    There is a specific set of parameters defined, although the server
    MAY choose to support query parameters not defined in this document.
    The contents of the any query parameter value MUST be encoded
    according to [RFC3986], Section 3.4. Any reserved characters MUST be
    percent-encoded, according to [RFC3986], section 2.1.

    o fragment: This field is not used by the RESTCONF protocol.

    When new resources are created by the client, a "Location" header is
    returned, which identifies the path of the newly created resource.
    The client uses this exact path identifier to access the resource
    once it has been created.

    The "target" of an operation is a resource. The "path" field in the
    request URI represents the target resource for the operation.
    """

    _allSchemes = ['http', 'https']
    _allMethods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS', 'HEAD']

    _parsedUrl = None
    _valid = True
    _errorMessage = ''

    _entry = None
    _resource = None
    _resource_api = None
    _query = None
    _queryParams = {}

    DEFAULT_METHOD = 'GET'
    DEFAULT_SCHEME = 'http'
    DEFAULT_API_ROOT = 'restconf'
    DATA_RESOURCE_API = 'data'
    OPERATIONS_RESOURCE_API = 'operations'
    LIBRARY_RESOURCE_API = 'yang-library-version'

    def __init__(self, url, method='GET', api_root='restconf'):
        self._method = method.upper()

        if self._method not in self._allMethods:
            self._valid = False
            self._errorMessage = '[%s] is not a valid RESTCONF operation/method' % self._method
            raise ValueError(self._errorMessage)

        # Parse as if http, specify all_fragments as true so that they are not
        # included in the preceding component.  RESTCONF ignores fragments

        self._parsedUrl = urlparse(url, scheme=RestconfUrl.DEFAULT_SCHEME, allow_fragments=True)

        # Now proceed with RESTCONF specific parsing

        self._entry = self._parse_entry(api_root)

        if self._valid:
            self._resource = self._parse_resource(api_root)

        if self._valid:
            self._query = self._parse_query()

    @staticmethod
    def create(url, method='GET', api_root='restconf'):
        # Validate method
        if method not in RestconfUrl._allMethods:
            raise ValueError('[%s] is not a valid RESTCONF operation/method' % method)

        # Validate scheme and api root
        parsed = urlparse(url, scheme=RestconfUrl.DEFAULT_SCHEME, allow_fragments=True)

        if parsed.scheme not in RestconfUrl._allSchemes:
            raise ValueError("Scheme '%s' not valid for RESTCONF" % parsed.scheme)

        # The API root should show up in the path and be the first part of it

        path = parsed.path()
        if path is None or not path.startswith(api_root):
            raise ValueError("URL path '%s' does not start RESTCONF API root '%s'" % (path, api_root))

        api = path[len(api_root):]

        if len(api) == 0 or (len(api) == 1 and api == '/'):
            return RestconfUrl(url, method=method, api_root=api_root)

        if api[1:len(RestconfUrl.DATA_RESOURCE_API)] == RestconfUrl.DATA_RESOURCE_API and \
                (len(api[1 + len(RestconfUrl.DATA_RESOURCE_API):]) == 0 or
                         api[1 + len(RestconfUrl.DATA_RESOURCE_API):1] == '/'):
            from restconfDataUrl import RestconfDataUrl
            return RestconfDataUrl(url, method=method, api_root=api_root)

        if api[1:len(RestconfUrl.OPERATIONS_RESOURCE_API)] == RestconfUrl.OPERATIONS_RESOURCE_API and \
                (len(api[1 + len(RestconfUrl.OPERATIONS_RESOURCE_API):]) == 0 or
                         api[1 + len(RestconfUrl.OPERATIONS_RESOURCE_API):1] == '/'):
            from restconfOperationUrl import RestconfOperationUrl
            return RestconfOperationUrl(url, method=method, api_root=api_root)

        if api[1:len(RestconfUrl.OPERATIONS_RESOURCE_API)] == RestconfUrl.OPERATIONS_RESOURCE_API and \
                (len(api[1 + len(RestconfUrl.OPERATIONS_RESOURCE_API):]) == 0 or
                         api[1 + len(RestconfUrl.OPERATIONS_RESOURCE_API):1] == '/'):
            from restconfLibraryUrl import RestconfLibraryUrl
            return RestconfLibraryUrl(url, method=method, api_root=api_root)

        raise ValueError("URL path '%s' does not start a valid RESTCONF API URI" % path)

    @property
    def is_valid(self):
        return self._valid

    @property
    def error_message(self):
        return self._errorMessage

    @property
    def method(self):
        """
        The HTTP method identifying the RESTCONF operation requested by the
        client, to act upon the target resource specified in the request URI.
        RESTCONF operation details are described in Section 4.

        The method is Mandatory

        :returns (string): The operational method being performed
        """
        return self._method

    @property
    def scheme(self):
        return self._parsedUrl.scheme.lower()

    def _parse_scheme(self):
        if self.scheme not in self._allSchemes:
            self._valid = False
            self._errorMessage = "Scheme '%s' not valid for RESTCONF" % self.scheme
            raise ValueError(self._errorMessage)

    @property
    def entry(self):
        """
        The root of the RESTCONF API configured on this HTTP server, discovered
        by getting the "/.well-known/host-meta" resource, as described in
        Section 3.1.

        The entry is Mandatory

        :returns (string): The resource API entry point
        """
        return self._entry

    def _parse_entry(self, api_root):
        # The API root should show up in the path and be the first part of it

        path = self._parsedUrl.path()

        if path is None or not path.startswith(api_root):
            self._valid = False
            self._errorMessage = "URL path '%s' does not start RESTCONF API root '%s'" % (path, api_root)
            raise ValueError(self._errorMessage)

        return api_root

    @property
    def resource(self):
        """
        The path expression identifying the resource that is being accessed by
        the operation. If this field is not present, then the target resource
        is the API itself, represented by the media type "application/yang.api".

        The resource is Optional

        :returns (string): The resource that is being accessed
        """
        return self._resource

    # TODO: For the resource, also parse out the module name (if any) and any initial containers
    # TODO: For the resource, also parse type if present ('data', 'operations', ...)

    def resource_api(self):
        """
        :returns: (None) The root API resource is None.  Derived classed provide the others
        """
        return None

    def _parse_resource(self, api_root):
        path = self._parsedUrl.path()

        if not path.startswith(api_root):
            self._valid = False
            self._errorMessage = "URL path '%s' does not start RESTCONF API root '%s'" % (path, api_root)
            raise ValueError(self._errorMessage)

        return path[len(api_root):]

    @property
    def query(self):
        """
        The set of parameters associated with the RESTCONF message. These have
        the familiar form of "name=value" pairs. Most query parameters are
        optional to implement by the server and optional to use by the client.
        Each optional query parameter is identified by a URI. The server MUST
        list the optional query parameter URIs it supports in the "capabilities"
        list defined in Section 9.3.

        The query is Optional

        Each RESTCONF operation allows zero or more query parameters to be
        present in the request URI.  The specific parameters that are allowed
        depends on the resource type, and sometimes the specific target resource
        used, in the request.

        +-------------------+-------------+---------------------------------+
        | Name              | Methods     | Description                     |
        +-------------------+-------------+---------------------------------+
        | content           | GET         | Select config and/or non-config |
        |                   |             | data resources                  |
        | depth             | GET         | Request limited sub-tree depth  |
        |                   |             | in the reply content            |
        | fields            | GET         | Request a subset of the target  |
        |                   |             | resource contents               |
        | filter            | GET         | Boolean notification filter for |
        |                   |             | event stream resources          |
        | insert            | POST, PUT   | Insertion mode for user-ordered |
        |                   |             | data resources                  |
        | point             | POST, PUT   | Insertion point for user-       |
        |                   |             | ordered data resources          |
        | start-time        | GET         | Replay buffer start time for    |
        |                   |             | event stream resources          |
        | stop-time         | GET         | Replay buffer stop time for     |
        |                   |             | event stream resources          |
        | with-defaults     | GET         | Control retrieval of default    |
        |                   |             | values                          |
        +-------------------+-------------+---------------------------------+
        """
        return self._query

    def _parse_query(self):
        return ''  # TODO Implement this
