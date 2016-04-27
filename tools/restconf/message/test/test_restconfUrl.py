#!/usr/bin/python
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
import unittest
from ..restconfUrl import RestconfUrl


class RestconfUrlTest(unittest.TestCase):
    def test_defaults(self):
        url = RestconfUrl('www.test.com/restconf')

        self.assertIsInstance(url, RestconfUrl)
        self.assertEqual(url.method, RestconfUrl.DEFAULT_METHOD)
        self.assertEqual(url.scheme, RestconfUrl.DEFAULT_SCHEME)
        self.assertEqual(url.entry, RestconfUrl.DEFAULT_API_ROOT)
        self.assertEqual(url.resource, '')
        self.assertDictEqual(url.query, {})

    def test_simple_init_value_exceptions(self):
        """
        Test several value exceptions that should be generated
        """
        self.assertRaises(ValueError, RestconfUrl('test.com/restconf', method='BAD'))
        self.assertRaises(ValueError, RestconfUrl('mailto:test@bcsw.net'))
        self.assertRaises(ValueError, RestconfUrl('test.com/restbad'))
        self.assertRaises(ValueError, RestconfUrl('http://test.com'))
        self.assertRaises(ValueError, RestconfUrl('https://test.com'))
        self.assertRaises(ValueError, RestconfUrl('test.com/restconf', api_root='not_restconf'))
        pass

    def test_api_root_resource(self):
        # ''
        self.assertEqual(RestconfUrl('test.com/restconf').resource, '')
        self.assertEqual(RestconfUrl('test.com/restconf').resource_api, None)

        # '/'
        self.assertEqual(RestconfUrl('test.com/restconf/').resource, '/')
        self.assertEqual(RestconfUrl('test.com/restconf/').resource_api, None)
        self.assertEqual(RestconfUrl('test.com/restconf/abcd').resource_api, None)

        # '/data'
        self.assertEqual(RestconfUrl('test.com/restconf/data').resource, '/data')
        self.assertEqual(RestconfUrl('test.com/restconf/data').resource_api, RestconfUrl.DATA_RESOURCE_API)
        self.assertEqual(RestconfUrl('test.com/restconf/data/abcd').resource_api, RestconfUrl.DATA_RESOURCE_API)

        # '/operations'
        self.assertEqual(RestconfUrl('test.com/restconf/operations').resource, '/operations')
        self.assertEqual(RestconfUrl('test.com/restconf/operations').resource_api, RestconfUrl.OPERATIONS_RESOURCE_API)
        self.assertEqual(RestconfUrl('test.com/restconf/operations/abcd').resource_api,
                         RestconfUrl.OPERATIONS_RESOURCE_API)

        # '/yang-library-version
        self.assertEqual(RestconfUrl('test.com/restconf/yang-library-version').resource, '/yang-library-version')
        self.assertEqual(RestconfUrl('test.com/restconf/yang-library-version').resource_api,
                         RestconfUrl.LIBRARY_RESOURCE_API)
        self.assertEqual(RestconfUrl('test.com/restconf/yang-library-version/abcd').resource_api,
                         RestconfUrl.LIBRARY_RESOURCE_API)
        pass

    def test_methods_with_api(self):
        # TODO Test base resource API for GET/POST/PUT/...
        # /restconf                         GET, HEAD, OPTIONS
        # /restconf/data                    GET, HEAD, POST, PUT, DELETE, PATCH, OPTIONS
        # /restconf/data/*                  GET, HEAD, POST, PUT, DELETE, PATCH, OPTIONS
        # /restconf/operations              -none-
        # /restconf/operations/*            POST, OPTIONS
        # /restconf/yang-library-version    GET, HEAD, OPTIONS
        # /restconf/yang-library-version/*  GET, HEAD, OPTIONS
        pass

    def test_resource_path_basics(self):
        # TODO Test for parsing good/bad paths at the /<path> - resource
        # It is optional (is this handled case in previous?)
        # Just the model name (is that optional)
        # Model + a container  (ie model:container)
        # model+container+more-levels (simple)
        # module:container/path/path/model2:path/...
        #
        #
        pass

    def test_resource_path_list_(self):
        # TODO Test for parsing good/bad paths that have a list
        # /restconf/data/top-leaflist=fred
        # /restconf/data/top-leaflist=fred/leaf
        # /restconf/data/top-leaflist=%22fred%22/leaf       # Quoted
        # /restconf/data/example-top:top/list1=key1,key2,key3/list2=key4,key5/leaf
        #
        # /restconf/data/example-top:top/Y=1234   (this is without keys, instance value)
        #
        pass

    def test_query_parameters_content(self):
        """
        +-------------------+-------------+---------------------------------+
        | Name              | Methods     | Description                     |
        +-------------------+-------------+---------------------------------+
        | content           | GET         | Select config and/or non-config |
        |                   |             | data resources                  |
        +-------------------+-------------+---------------------------------+

        The "content" parameter controls how descendant nodes of the
        requested data nodes will be processed in the reply.

        The allowed values are:

        +-----------+-----------------------------------------------------+
        | Value     | Description                                         |
        +-----------+-----------------------------------------------------+
        | config    | Return only configuration descendant data nodes     |
        | nonconfig | Return only non-configuration descendant data nodes |
        | all       | Return all descendant data nodes                    |
        +-----------+-----------------------------------------------------+

        This parameter is only allowed for GET methods on datastore and data
        resources.  A '400 Bad Request' status-line is returned if used for
        other methods or resource types.

        If this query parameter is not present, the default value is 'all'.
        This query parameter MUST be supported by the server.
        """
        # TODO: simple tests first
        pass

    def test_query_parameters_depth(self):
        """
        +-------------------+-------------+---------------------------------+
        | Name              | Methods     | Description                     |
        +-------------------+-------------+---------------------------------+
        | depth             | GET         | Request limited sub-tree depth  |
        |                   |             | in the reply content            |
        +-------------------+-------------+---------------------------------+

        The "depth" parameter is used to specify the number of nest levels
        returned in a response for a GET method.  The first nest-level
        consists of the requested data node itself.  If the "fields"
        parameter (Section 4.8.3) is used to select descendant data nodes,
        these nodes all have a depth value of 1.  This has the effect of
        including the nodes specified by the fields, even if the "depth"
        value is less than the actual depth level of the specified fields.
        Any child nodes which are contained within a parent node have a depth
        value that is 1 greater than its parent.

        The value of the "depth" parameter is either an integer between 1 and
        65535, or the string "unbounded".  "unbounded" is the default.

        This parameter is only allowed for GET methods on API, datastore, and
        data resources.  A "400 Bad Request" status-line is returned if it
        used for other methods or resource types.

        More than one "depth" query parameter MUST NOT appear in a request.
        If more than one instance is present, then a "400 Bad Request"
        status-line MUST be returned by the server.

        By default, the server will include all sub-resources within a
        retrieved resource, which have the same resource type as the
        requested resource.  Only one level of sub-resources with a different
        media type than the target resource will be returned.

        If the "depth" query parameter URI is listed in the "capability"
        leaf-list in Section 9.3, then the server supports the "depth" query
        parameter.
        """
        # TODO: simple tests first
        pass

    def test_query_parameters_fields(self):
        """
        +-------------------+-------------+---------------------------------+
        | Name              | Methods     | Description                     |
        +-------------------+-------------+---------------------------------+
        | fields            | GET         | Request a subset of the target  |
        |                   |             | resource contents               |
        +-------------------+-------------+---------------------------------+

        The "fields" query parameter is used to optionally identify data
        nodes within the target resource to be retrieved in a GET method.
        The client can use this parameter to retrieve a subset of all nodes
        in a resource.

        A value of the "fields" query parameter matches the following rule:

        fields-expr = path '(' fields-expr ')' /
                      path ';' fields-expr /
                      path
        path = api-identifier [ '/' path ]

        "api-identifier" is defined in Section 3.5.1.1.

        ";" is used to select multiple nodes.  For example, to retrieve only
        the "genre" and "year" of an album, use: "fields=genre;year".

        Parentheses are used to specify sub-selectors of a node.

        For example, assume the target resource is the "album" list.  To
        retrieve only the "label" and "catalogue-number" of the "admin"
        container within an album, use:
        "fields=admin(label;catalogue-number)".

        "/" is used in a path to retrieve a child node of a node.  For
        example, to retrieve only the "label" of an album, use: "fields=admin
        /label".

        This parameter is only allowed for GET methods on api, datastore, and
        data resources.  A "400 Bad Request" status-line is returned if used
        for other methods or resource types.

        More than one "fields" query parameter MUST NOT appear in a request.
        If more than one instance is present, then a "400 Bad Request"
        status-line MUST be returned by the server.

        If the "fields" query parameter URI is listed in the "capability"
        leaf-list in Section 9.3, then the server supports the "fields"
        parameter.
        """
        # TODO: simple tests first
        pass

    def test_query_parameters_filter(self):
        """
        +-------------------+-------------+---------------------------------+
        | Name              | Methods     | Description                     |
        +-------------------+-------------+---------------------------------+
        | filter            | GET         | Boolean notification filter for |
        |                   |             | event stream resources          |
        +-------------------+-------------+---------------------------------+

        The "filter" parameter is used to indicate which subset of all
        possible events are of interest.  If not present, all events not
        precluded by other parameters will be sent.

        This parameter is only allowed for GET methods on a text/event-stream
        data resource.  A "400 Bad Request" status-line is returned if used
        for other methods or resource types.

        The format of this parameter is an XPath 1.0 expression, and is
        evaluated in the following context:

        o  The set of namespace declarations is the set of prefix and
           namespace pairs for all supported YANG modules, where the prefix
           is the YANG module name, and the namespace is as defined by the
           "namespace" statement in the YANG module.

        o  The function library is the core function library defined in XPath
          1.0.

        o  The set of variable bindings is empty.

        o  The context node is the root node.

        More than one "filter" query parameter MUST NOT appear in a request.
        If more than one instance is present, then a "400 Bad Request"
        status-line MUST be returned by the server.

        The filter is used as defined in [RFC5277], Section 3.6.  If the
        boolean result of the expression is true when applied to the
        conceptual "notification" document root, then the event notification
        is delivered to the client.

        If the "filter" query parameter URI is listed in the "capability"
        leaf-list in Section 9.3, then the server supports the "filter" query
        parameter.
        """
        # TODO: simple tests first
        pass

    def test_query_parameters_insert(self):
        """
        +-------------------+-------------+---------------------------------+
        | Name              | Methods     | Description                     |
        +-------------------+-------------+---------------------------------+
        | insert            | POST, PUT   | Insertion mode for user-ordered |
        |                   |             | data resources                  |
        +-------------------+-------------+---------------------------------+
        The "insert" parameter is used to specify how a resource should be
        inserted within a user-ordered list.

        The allowed values are:

        +-----------+-------------------------------------------------------+
        | Value     | Description                                           |
        +-----------+-------------------------------------------------------+
        | first     | Insert the new data as the new first entry.           |
        | last      | Insert the new data as the new last entry.            |
        | before    | Insert the new data before the insertion point, as    |
        |           | specified by the value of the "point" parameter.      |
        | after     | Insert the new data after the insertion point, as     |
        |           | specified by the value of the "point" parameter.      |
        +-----------+-------------------------------------------------------+

        The default value is "last".

        This parameter is only supported for the POST and PUT methods.  It is
        also only supported if the target resource is a data resource, and
        that data represents a YANG list or leaf-list that is ordered by the
        user.

        More than one "insert" query parameter MUST NOT appear in a request.
        If more than one instance is present, then a "400 Bad Request"
        status-line MUST be returned by the server.

        If the values "before" or "after" are used, then a "point" query
        parameter for the insertion parameter MUST also be present, or a "400
        Bad Request" status-line is returned.

        The "insert" query parameter MUST be supported by the server.
        """
        # TODO: simple tests first
        pass

    def test_query_parameters_point(self):
        """
        +-------------------+-------------+---------------------------------+
        | Name              | Methods     | Description                     |
        +-------------------+-------------+---------------------------------+
        | point             | POST, PUT   | Insertion point for user-       |
        |                   |             | ordered data resources          |
        +-------------------+-------------+---------------------------------+

        The "point" parameter is used to specify the insertion point for a
        data resource that is being created or moved within a user ordered
        list or leaf-list.

        The value of the "point" parameter is a string that identifies the
        path to the insertion point object.  The format is the same as a
        target resource URI string.

        This parameter is only supported for the POST and PUT methods.  It is
        also only supported if the target resource is a data resource, and
        that data represents a YANG list or leaf-list that is ordered by the
        user.

        If the "insert" query parameter is not present, or has a value other
        than "before" or "after", then a "400 Bad Request" status-line is
        returned.

        More than one "point" query parameter MUST NOT appear in a request.
        If more than one instance is present, then a "400 Bad Request"
        status-line MUST be returned by the server.

        This parameter contains the instance identifier of the resource to be
        used as the insertion point for a POST or PUT method.

        The "point" query parameter MUST be supported by the server.
        """
        # TODO: simple tests first
        pass

    def test_query_parameters_start_time(self):
        """
        +-------------------+-------------+---------------------------------+
        | Name              | Methods     | Description                     |
        +-------------------+-------------+---------------------------------+
        | start-time        | GET         | Replay buffer start time for    |
        |                   |             | event stream resources          |
        +-------------------+-------------+---------------------------------+

        The "start-time" parameter is used to trigger the notification replay
        feature and indicate that the replay should start at the time
        specified.  If the stream does not support replay, per the
        "replay-support" attribute returned by stream list entry for the
        stream resource, then the server MUST return a "400 Bad Request"
        status-line.

        The value of the "start-time" parameter is of type "date-and-time",
        defined in the "ietf-yang" YANG module [RFC6991].

        This parameter is only allowed for GET methods on a text/event-stream
        data resource.  A "400 Bad Request" status-line is returned if used
        for other methods or resource types.

        More than one "start-time" query parameter MUST NOT appear in a
        request.  If more than one instance is present, then a "400 Bad
        Request" status-line MUST be returned by the server.

        If this parameter is not present, then a replay subscription is not
        being requested.  It is not valid to specify start times that are
        later than the current time.  If the value specified is earlier than
        the log can support, the replay will begin with the earliest
        available notification.

        If this query parameter is supported by the server, then the "replay"
        query parameter URI MUST be listed in the "capability" leaf-list in
        Section 9.3.  The "stop-time" query parameter MUST also be supported
        by the server.

        If the "replay-support" leaf is present in the "stream" entry
        (defined in Section 9.3) then the server MUST support the
        "start-time" and "stop-time" query parameters for that stream.
        """
        # TODO: simple tests first
        pass

    def test_query_parameters_stop_time(self):
        """
        +-------------------+-------------+---------------------------------+
        | Name              | Methods     | Description                     |
        +-------------------+-------------+---------------------------------+
        | stop-time         | GET         | Replay buffer stop time for     |
        |                   |             | event stream resources          |
        +-------------------+-------------+---------------------------------+

        The "stop-time" parameter is used with the replay feature to indicate
        the newest notifications of interest.  This parameter MUST be used
        with and have a value later than the "start-time" parameter.

        The value of the "stop-time" parameter is of type "date-and-time",
        defined in the "ietf-yang" YANG module [RFC6991].

        This parameter is only allowed for GET methods on a text/event-stream
        data resource.  A "400 Bad Request" status-line is returned if used
        for other methods or resource types.

        More than one "stop-time" query parameter MUST NOT appear in a
        request.  If more than one instance is present, then a "400 Bad
        Request" status-line MUST be returned by the server.

        If this parameter is not present, the notifications will continue
        until the subscription is terminated.  Values in the future are
        valid.

        If this query parameter is supported by the server, then the "replay"
        query parameter URI MUST be listed in the "capability" leaf-list in
        Section 9.3.  The "start-time" query parameter MUST also be supported
        by the server.

        If the "replay-support" leaf is present in the "stream" entry
        (defined in Section 9.3) then the server MUST support the
        "start-time" and "stop-time" query parameters for that stream.
        """
        # TODO: simple tests first
        pass

    def test_query_parameters_with_defaults(self):
        """
        +-------------------+-------------+---------------------------------+
        | Name              | Methods     | Description                     |
        +-------------------+-------------+---------------------------------+
        | with-defaults     | GET         | Control retrieval of default    |
        |                   |             | values                          |
        +-------------------+-------------+---------------------------------+

        The "with-defaults" parameter is used to specify how information
        about default data nodes should be returned in response to GET
        requests on data resources.

        If the server supports this capability, then it MUST implement the
        behavior in Section 4.5.1 of [RFC6243], except applied to the
        RESTCONF GET operation, instead of the NETCONF operations.

        +---------------------------+---------------------------------------+
        | Value                     | Description                           |
        +---------------------------+---------------------------------------+
        | report-all                | All data nodes are reported           |
        | trim                      | Data nodes set to the YANG default    |
        |                           | are not reported                      |
        | explicit                  | Data nodes set to the YANG default by |
        |                           | the client are reported               |
        | report-all-tagged         | All data nodes are reported and       |
        |                           | defaults are tagged                   |
        +---------------------------+---------------------------------------+

        If the "with-defaults" parameter is set to "report-all" then the
        server MUST adhere to the defaults reporting behavior defined in
        Section 3.1 of [RFC6243].

        If the "with-defaults" parameter is set to "trim" then the server
        MUST adhere to the defaults reporting behavior defined in Section 3.2
        of [RFC6243].

        If the "with-defaults" parameter is set to "explicit" then the server
        MUST adhere to the defaults reporting behavior defined in Section 3.3
        of [RFC6243].

        If the "with-defaults" parameter is set to "report-all-tagged" then
        the server MUST adhere to the defaults reporting behavior defined in
        Section 3.4 of [RFC6243].

        More than one "with-defaults" query parameter MUST NOT appear in a
        request.  If more than one instance is present, then a "400 Bad
        Request" status-line MUST be returned by the server.

        If the "with-defaults" parameter is not present then the server MUST
        adhere to the defaults reporting behavior defined in its "basic-mode"
        parameter for the "defaults" protocol capability URI, defined in
        Section 9.1.2.

        If the server includes the "with-defaults" query parameter URI in the
        "capability" leaf-list in Section 9.3, then the "with-defaults" query
        parameter MUST be supported.
        """
        # TODO: simple tests first
        pass


if __name__ == '__main__':
    unittest.main()


# 4.8.  Query Parameters
#
#    Each RESTCONF operation allows zero or more query parameters to be
#    present in the request URI.  The specific parameters that are allowed
#    depends on the resource type, and sometimes the specific target
#    resource used, in the request.
#
#    +-------------------+-------------+---------------------------------+
#    | Name              | Methods     | Description                     |
#    +-------------------+-------------+---------------------------------+
#
#                          RESTCONF Query Parameters
#
#    Query parameters can be given in any order.  Each parameter can
#    appear at most once in a request URI.  A default value may apply if
#    the parameter is missing.
#
#    Refer to Appendix D.3 for examples of query parameter usage.
#
#    If vendors define additional query parameters, they SHOULD use a
#    prefix (such as the enterprise or organization name) for query
#    parameter names in order to avoid collisions with other parameters.



#
# 5.  Messages
#
#    The RESTCONF protocol uses HTTP entities for messages.  A single HTTP
#    message corresponds to a single protocol method.  Most messages can
#    perform a single task on a single resource, such as retrieving a
#    resource or editing a resource.  The exception is the PATCH method,
#    which allows multiple datastore edits within a single message.
#
# 5.1.  Request URI Structure
#
#    Resources are represented with URIs following the structure for
#    generic URIs in [RFC3986].
#
#    A RESTCONF operation is derived from the HTTP method and the request
#    URI, using the following conceptual fields:
#
#      <OP> /<restconf>/<path>?<query>#<fragment>
#
#          ^       ^        ^       ^         ^
#          |       |        |       |         |
#        method  entry  resource  query    fragment
#
#          M       M        O        O         I
#
#        M=mandatory, O=optional, I=ignored
#
#        where:
#
#       <OP> is the HTTP method
#       <restconf> is the RESTCONF entry point
#       <path> is the Target Resource URI
#       <query> is the query parameter list
#       <fragment> is not used in RESTCONF
#
#    o  method: the HTTP method identifying the RESTCONF operation
#       requested by the client, to act upon the target resource specified
#       in the request URI.  RESTCONF operation details are described in
#       Section 4.
#
#    o  entry: the root of the RESTCONF API configured on this HTTP
#       server, discovered by getting the "/.well-known/host-meta"
#       resource, as described in Section 3.1.
#
#    o  resource: the path expression identifying the resource that is
#       being accessed by the operation.  If this field is not present,
#       then the target resource is the API itself, represented by the
#       media type "application/yang.api".
#
#    o  query: the set of parameters associated with the RESTCONF message.
#       These have the familiar form of "name=value" pairs.  Most query
#       parameters are optional to implement by the server and optional to
#       use by the client.  Each optional query parameter is identified by
#       a URI.  The server MUST list the optional query parameter URIs it
#       supports in the "capabilities" list defined in Section 9.3.
#
#    There is a specific set of parameters defined, although the server
#    MAY choose to support query parameters not defined in this document.
#    The contents of the any query parameter value MUST be encoded
#    according to [RFC3986], Section 3.4.  Any reserved characters MUST be
#    percent-encoded, according to [RFC3986], section 2.1.
#
#    o  fragment: This field is not used by the RESTCONF protocol.
#
#    When new resources are created by the client, a "Location" header is
#    returned, which identifies the path of the newly created resource.
#    The client uses this exact path identifier to access the resource
#    once it has been created.
#
#    The "target" of an operation is a resource.  The "path" field in the
#    request URI represents the target resource for the operation.
#
#    Refer to Appendix D for examples of RESTCONF Request URIs.
#
#
#
#
#
# 5.3.  RESTCONF Meta-Data
#
#    The RESTCONF protocol needs to retrieve the same meta-data that is
#    used in the NETCONF protocol.  Information about default leafs, last-
#    modified timestamps, etc. are commonly used to annotate
#    representations of the datastore contents.  This meta-data is not
#    defined in the YANG schema because it applies to the datastore, and
#    is common across all data nodes.
#
#    This information is encoded as attributes in XML.  JSON encoding of
#    meta-data is defined in [I-D.ietf-netmod-yang-metadata].
#
#    The following examples are based on the example in Appendix D.3.9.
#    The "report-all-tagged" mode for the "with-defaults" query parameter
#    requires that a "default" attribute be returned for default nodes.
#    This example shows that attribute for the "mtu" leaf .
#
# 5.3.1.  XML MetaData Encoding Example
#
#    GET /restconf/data/interfaces/interface=eth1
#        ?with-defaults=report-all-tagged HTTP/1.1
#    Host: example.com
#    Accept: application/yang.data+xml
#
#    The server might respond as follows.
#
#    HTTP/1.1 200 OK
#    Date: Mon, 23 Apr 2012 17:01:00 GMT
#    Server: example-server
#    Content-Type: application/yang.data+xml
#
#    <interface
#      xmlns="urn:example.com:params:xml:ns:yang:example-interface">
#      <name>eth1</name>
#      <mtu xmlns:wd="urn:ietf:params:xml:ns:netconf:default:1.0"
#        wd:default="true">1500</mtu>
#      <status>up</status>
#    </interface>
#
#
# 5.3.2.  JSON MetaData Encoding Example
#
#    Note that RFC 6243 defines the "default" attribute with XSD, not
#    YANG, so the YANG module name has to be assigned manually.  The value
#    "ietf-netconf-with-defaults" is assigned for JSON meta-data encoding.
#
#    GET /restconf/data/interfaces/interface=eth1
#        ?with-defaults=report-all-tagged HTTP/1.1
#    Host: example.com
#    Accept: application/yang.data+json
#
#    The server might respond as follows.
#
#       HTTP/1.1 200 OK
#       Date: Mon, 23 Apr 2012 17:01:00 GMT
#       Server: example-server
#       Content-Type: application/yang.data+json
#
#       {
#         "example:interface": [
#           {
#             "name" : "eth1",
#             "mtu" : 1500,
#             "@mtu": {
#                "ietf-netconf-with-defaults:default" : true
#             },
#             "status" : "up"
#           }
#         ]
#       }
#
#
# 7.  Error Reporting
#
#    HTTP status-lines are used to report success or failure for RESTCONF
#    operations.  The <rpc-error> element returned in NETCONF error
#    responses contains some useful information.  This error information
#    is adapted for use in RESTCONF, and error information is returned for
#    "4xx" class of status codes.
#
#    The following table summarizes the return status codes used
#    specifically by RESTCONF operations:
#
#    +----------------------------+--------------------------------------+
#    | Status-Line                | Description                          |
#    +----------------------------+--------------------------------------+
#    | 100 Continue               | POST accepted, 201 should follow     |
#    | 200 OK                     | Success with response message-body   |
#    | 201 Created                | POST to create a resource success    |
#    | 204 No Content             | Success without response message-    |
#    |                            | body                                 |
#    | 304 Not Modified           | Conditional operation not done       |
#    | 400 Bad Request            | Invalid request message              |
#    | 401 Unauthorized           | Client cannot be authenticated       |
#    | 403 Forbidden              | Access to resource denied            |
#    | 404 Not Found              | Resource target or resource node not |
#    |                            | found                                |
#    | 405 Method Not Allowed     | Method not allowed for target        |
#    |                            | resource                             |
#    | 409 Conflict               | Resource or lock in use              |
#    | 412 Precondition Failed    | Conditional method is false          |
#    | 413 Request Entity Too     | too-big error                        |
#    | Large                      |                                      |
#    | 414 Request-URI Too Large  | too-big error                        |
#    | 415 Unsupported Media Type | non RESTCONF media type              |
#    | 500 Internal Server Error  | operation-failed                     |
#    | 501 Not Implemented        | unknown-operation                    |
#    | 503 Service Unavailable    | Recoverable server error             |
#    +----------------------------+--------------------------------------+
#
#                     HTTP Status Codes used in RESTCONF
#
#    Since an operation resource is defined with a YANG "rpc" statement,
#    and an action is defined with a YANG "action" statement, a mapping
#    between the NETCONF <error-tag> value and the HTTP status code is
#    needed.  The specific error condition and response code to use are
#    data-model specific and might be contained in the YANG "description"
#    statement for the "action" or "rpc" statement.
#
#                  +-------------------------+-------------+
#                  | <error&#8209;tag>       | status code |
#                  +-------------------------+-------------+
#                  | in-use                  | 409         |
#                  | invalid-value           | 400         |
#                  | too-big                 | 413         |
#                  | missing-attribute       | 400         |
#                  | bad-attribute           | 400         |
#                  | unknown-attribute       | 400         |
#                  | bad-element             | 400         |
#                  | unknown-element         | 400         |
#                  | unknown-namespace       | 400         |
#                  | access-denied           | 403         |
#                  | lock-denied             | 409         |
#                  | resource-denied         | 409         |
#                  | rollback-failed         | 500         |
#                  | data-exists             | 409         |
#                  | data-missing            | 409         |
#                  | operation-not-supported | 501         |
#                  | operation-failed        | 500         |
#                  | partial-operation       | 500         |
#                  | malformed-message       | 400         |
#                  +-------------------------+-------------+
#
#                    Mapping from error-tag to status code
#
# 7.1.  Error Response Message
#
#    When an error occurs for a request message on a data resource or an
#    operation resource, and a "4xx" class of status codes will be
#    returned (except for status code "403 Forbidden"), then the server
#    SHOULD send a response message-body containing the information
#    described by the "errors" container definition within the YANG module
#    Section 8.  The Content-Type of this response message MUST be
#    application/yang.errors (see example below).
#
#    The client MAY specify the desired encoding for error messages by
#    specifying the appropriate media-type in the Accept header.  If no
#    error media is specified, then the media type of the request message
#    SHOULD be used, or the server MAY choose any supported message
#    encoding format.  If there is no request message the server MUST
#    select "application/yang.errors+xml" or "application/
#    yang.errors+json", depending on server preference.  All of the
#    examples in this document, except for the one below, assume that XML
#    encoding will be returned if there is an error.
#
#    YANG Tree Diagram for <errors> data:
#
#    +--ro errors
#       +--ro error*
#          +--ro error-type       enumeration
#          +--ro error-tag        string
#          +--ro error-app-tag?   string
#          +--ro error-path?      instance-identifier
#          +--ro error-message?   string
#          +--ro error-info
#
#    The semantics and syntax for RESTCONF error messages are defined in
#    the "application/yang.errors" restconf-media-type extension in
#    Section 8.
#
#    Examples:
#
#    The following example shows an error returned for an "lock-denied"
#    error that can occur if a NETCONF client has locked a datastore.  The
#    RESTCONF client is attempting to delete a data resource.  Note that
#    an Accept header is used to specify the desired encoding for the
#    error message.  This example's use of the Accept header is especially
#    notable since the DELETE method typically doesn't return a message-
#    body and hence Accept headers are typically not passed.
#
#    DELETE /restconf/data/example-jukebox:jukebox/
#       library/artist=Foo%20Fighters/album=Wasting%20Light HTTP/1.1
#    Host: example.com
#    Accept: application/yang.errors+json
#
#    The server might respond:
#
#       HTTP/1.1 409 Conflict
#       Date: Mon, 23 Apr 2012 17:11:00 GMT
#       Server: example-server
#       Content-Type: application/yang.errors+json
#
#       {
#         "ietf-restconf:errors": {
#           "error": [
#             {
#               "error-type": "protocol",
#               "error-tag": "lock-denied",
#               "error-message": "Lock failed, lock already held"
#             }
#           ]
#         }
#       }
#
#    The following example shows an error returned for a "data-exists"
#    error on a data resource.  The "jukebox" resource already exists so
#    it cannot be created.
#
#    The client might send:
#
#    POST /restconf/data/example-jukebox:jukebox HTTP/1.1
#    Host: example.com
#
#    The server might respond (some lines wrapped for display purposes):
#
#    HTTP/1.1 409 Conflict
#    Date: Mon, 23 Apr 2012 17:11:00 GMT
#    Server: example-server
#    Content-Type: application/yang.errors+xml
#
#    <errors xmlns="urn:ietf:params:xml:ns:yang:ietf-restconf">
#      <error>
#        <error-type>protocol</error-type>
#        <error-tag>data-exists</error-tag>
#        <error-path
#          xmlns:rc="urn:ietf:params:xml:ns:yang:ietf-restconf"
#          xmlns:jbox="https://example.com/ns/example-jukebox">
#          /rc:restconf/rc:data/jbox:jukebox
#        </error-path>
#        <error-message>
#          Data already exists, cannot create new resource
#        </error-message>
#      </error>
#    </errors>
#
#
#
#
#
#
#
#
# Appendix D.  RESTCONF Message Examples
#
#    The examples within this document use the normative YANG module
#    defined in Section 8 and the non-normative example YANG module
#    defined in Appendix C.1.
#
#    This section shows some typical RESTCONF message exchanges.
#
#
# D.1.  Resource Retrieval Examples
#
# D.1.1.  Retrieve the Top-level API Resource
#
#    The client may start by retrieving the top-level API resource, using
#    the entry point URI "{+restconf}".
#
#    GET /restconf   HTTP/1.1
#    Host: example.com
#    Accept: application/yang.api+json
#
#    The server might respond as follows:
#
#       HTTP/1.1 200 OK
#       Date: Mon, 23 Apr 2012 17:01:00 GMT
#       Server: example-server
#       Content-Type: application/yang.api+json
#
#       {
#         "ietf-restconf:restconf": {
#           "data" : {},
#           "operations" : {}
#         }
#       }
#
#    To request that the response content to be encoded in XML, the
#    "Accept" header can be used, as in this example request:
#
#    GET /restconf HTTP/1.1
#    Host: example.com
#    Accept: application/yang.api+xml
#
#    The server will return the same response either way, which might be
#    as follows :
#
#    HTTP/1.1 200 OK
#    Date: Mon, 23 Apr 2012 17:01:00 GMT
#    Server: example-server
#    Cache-Control: no-cache
#    Pragma: no-cache
#    Content-Type: application/yang.api+xml
#
#    <restconf xmlns="urn:ietf:params:xml:ns:yang:ietf-restconf">
#      <data/>
#      <operations/>
#      <yang-library-version>2016-02-01</yang-library-version>
#    </restconf>
#
#
# D.1.2.  Retrieve The Server Module Information
#
#    In this example the client is retrieving the modules information from
#    the server in JSON format:
#
#    GET /restconf/data/ietf-yang-library:modules HTTP/1.1
#    Host: example.com
#    Accept: application/yang.data+json
#
#    The server might respond as follows (some strings wrapped for display
#    purposes):
#
#       HTTP/1.1 200 OK
#       Date: Mon, 23 Apr 2012 17:01:00 GMT
#       Server: example-server
#       Cache-Control: no-cache
#       Pragma: no-cache
#       Last-Modified: Sun, 22 Apr 2012 01:00:14 GMT
#       Content-Type: application/yang.data+json
#
#       {
#         "ietf-yang-library:modules": {
#           "module": [
#             {
#               "name" : "foo",
#               "revision" : "2012-01-02",
#               "schema" : "https://example.com/modules/foo/2012-01-02",
#               "namespace" : "http://example.com/ns/foo",
#               "feature" : [ "feature1", "feature2" ],
#               "conformance-type" : "implement"
#             },
#             {
#               "name" : "ietf-yang-library",
#               "revision" : "2016-02-01",
#               "schema" : "https://example.com/modules/ietf-yang-
#                 library/2016-02-01",
#               "namespace" :
#                 "urn:ietf:params:xml:ns:yang:ietf-yang-library",
#               "conformance-type" : "implement"
#             },
#             {
#               "name" : "foo-types",
#               "revision" : "2012-01-05",
#               "schema" :
#                 "https://example.com/modules/foo-types/2012-01-05",
#               "namespace" : "http://example.com/ns/foo-types",
#               "conformance-type" : "import"
#             },
#             {
#               "name" : "bar",
#               "revision" : "2012-11-05",
#               "schema" : "https://example.com/modules/bar/2012-11-05",
#               "namespace" : "http://example.com/ns/bar",
#               "feature" : [ "bar-ext" ],
#               "conformance-type" : "implement",
#               "submodule" : [
#                 {
#                   "name" : "bar-submod1",
#                   "revision" : "2012-11-05",
#                   "schema" :
#                    "https://example.com/modules/bar-submod1/2012-11-05"
#                 },
#                 {
#                   "name" : "bar-submod2",
#                   "revision" : "2012-11-05",
#                   "schema" :
#                    "https://example.com/modules/bar-submod2/2012-11-05"
#                 }
#               ]
#             }
#           ]
#         }
#       }
#
# D.1.3.  Retrieve The Server Capability Information
#
#    In this example the client is retrieving the capability information
#    from the server in XML format, and the server supports all the
#    RESTCONF query parameters, plus one vendor parameter:
#
#    GET /restconf/data/ietf-restconf-monitoring:restconf-state/
#        capabilities  HTTP/1.1
#    Host: example.com
#    Accept: application/yang.data+xml
#
#    The server might respond as follows.  The extra whitespace in
#    'capability' elements for display purposes only.
#
#    HTTP/1.1 200 OK
#    Date: Mon, 23 Apr 2012 17:02:00 GMT
#    Server: example-server
#    Cache-Control: no-cache
#    Pragma: no-cache
#    Last-Modified: Sun, 22 Apr 2012 01:00:14 GMT
#    Content-Type: application/yang.data+xml
#
#    <capabilities xmlns="">
#     <capability>
#      urn:ietf:params:restconf:capability:depth:1.0
#     </capability>
#     <capability>
#      urn:ietf:params:restconf:capability:fields:1.0
#     </capability>
#     <capability>
#      urn:ietf:params:restconf:capability:filter:1.0
#     </capability>
#     <capability>
#      urn:ietf:params:restconf:capability:start-time:1.0
#     </capability>
#     <capability>
#      urn:ietf:params:restconf:capability:stop-time:1.0
#     </capability>
#     <capability>
#      http://example.com/capabilities/myparam
#     </capability>
#    </capabilities>
#
# D.2.  Edit Resource Examples
#
# D.2.1.  Create New Data Resources
#
#    To create a new "artist" resource within the "library" resource, the
#    client might send the following request.
#
#       POST /restconf/data/example-jukebox:jukebox/library HTTP/1.1
#       Host: example.com
#       Content-Type: application/yang.data+json
#
#       {
#         "example-jukebox:artist" : {
#           "name" : "Foo Fighters"
#         }
#       }
#
#    If the resource is created, the server might respond as follows.
#    Note that the "Location" header line is wrapped for display purposes
#    only:
#
#    HTTP/1.1 201 Created
#    Date: Mon, 23 Apr 2012 17:02:00 GMT
#    Server: example-server
#    Location: https://example.com/restconf/data/
#        example-jukebox:jukebox/library/artist=Foo%20Fighters
#    Last-Modified: Mon, 23 Apr 2012 17:02:00 GMT
#    ETag: b3830f23a4c
#
#    To create a new "album" resource for this artist within the "jukebox"
#    resource, the client might send the following request.  Note that the
#    request URI header line is wrapped for display purposes only:
#
#    POST /restconf/data/example-jukebox:jukebox/
#        library/artist=Foo%20Fighters  HTTP/1.1
#    Host: example.com
#    Content-Type: application/yang.data+xml
#
#    <album xmlns="http://example.com/ns/example-jukebox">
#      <name>Wasting Light</name>
#      <year>2011</year>
#    </album>
#
#    If the resource is created, the server might respond as follows.
#    Note that the "Location" header line is wrapped for display purposes
#    only:
#
#    HTTP/1.1 201 Created
#    Date: Mon, 23 Apr 2012 17:03:00 GMT
#    Server: example-server
#    Location: https://example.com/restconf/data/
#        example-jukebox:jukebox/library/artist=Foo%20Fighters/
#        album=Wasting%20Light
#    Last-Modified: Mon, 23 Apr 2012 17:03:00 GMT
#    ETag: b8389233a4c
#
# D.2.2.  Detect Resource Entity Tag Change
#
#    In this example, the server just supports the mandatory datastore
#    last-changed timestamp.  The client has previously retrieved the
#    "Last-Modified" header and has some value cached to provide in the
#    following request to patch an "album" list entry with key value
#    "Wasting Light".  Only the "genre" field is being updated.
#
#       PATCH /restconf/data/example-jukebox:jukebox/
#           library/artist=Foo%20Fighters/album=Wasting%20Light/genre
#           HTTP/1.1
#       Host: example.com
#       If-Unmodified-Since: Mon, 23 Apr 2012 17:01:00 GMT
#
#       Content-Type: application/yang.data+json
#
#       { "example-jukebox:genre" : "example-jukebox:alternative" }
#
#    In this example the datastore resource has changed since the time
#    specified in the "If-Unmodified-Since" header.  The server might
#    respond:
#
#    HTTP/1.1 412 Precondition Failed
#    Date: Mon, 23 Apr 2012 19:01:00 GMT
#    Server: example-server
#    Last-Modified: Mon, 23 Apr 2012 17:45:00 GMT
#    ETag: b34aed893a4c
#
# D.2.3.  Edit a Datastore Resource
#
#    In this example, the client modifies two different data nodes by
#    sending a PATCH to the datastore resource:
#
#    PATCH /restconf/data HTTP/1.1
#    Host: example.com
#    Content-Type: application/yang.datastore+xml
#
#    <data xmlns="urn:ietf:params:xml:ns:yang:ietf-restconf">
#      <jukebox xmlns="http://example.com/ns/example-jukebox">
#        <library>
#          <artist>
#            <name>Foo Fighters</name>
#            <album>
#              <name>Wasting Light</name>
#              <year>2011</year>
#            </album>
#          </artist>
#          <artist>
#            <name>Nick Cave</name>
#            <album>
#              <name>Tender Prey</name>
#              <year>1988</year>
#            </album>
#          </artist>
#        </library>
#      </jukebox>
#    </data>
#
# D.3.  Query Parameter Examples
#
# D.3.1.  "content" Parameter
#
#    The "content" parameter is used to select the type of data child
#    resources (configuration and/or not configuration) that are returned
#    by the server for a GET method request.
#
#    In this example, a simple YANG list that has configuration and non-
#    configuration child resources.
#
#    container events
#      list event {
#        key name;
#        leaf name { type string; }
#        leaf description { type string; }
#        leaf event-count {
#          type uint32;
#          config false;
#        }
#      }
#    }
#
#    Example 1: content=all
#
#    To retrieve all the child resources, the "content" parameter is set
#    to "all".  The client might send:
#
#    GET /restconf/data/example-events:events?content=all
#        HTTP/1.1
#    Host: example.com
#    Accept: application/yang.data+json
#
#    The server might respond:
#
#       HTTP/1.1 200 OK
#       Date: Mon, 23 Apr 2012 17:11:30 GMT
#       Server: example-server
#       Cache-Control: no-cache
#       Pragma: no-cache
#       Content-Type: application/yang.data+json
#
#       {
#         "example-events:events" : {
#           "event" : [
#             {
#               "name" : "interface-up",
#               "description" : "Interface up notification count",
#               "event-count" : 42
#             },
#             {
#               "name" : "interface-down",
#               "description" : "Interface down notification count",
#               "event-count" : 4
#             }
#           ]
#         }
#       }
#
#    Example 2: content=config
#
#    To retrieve only the configuration child resources, the "content"
#    parameter is set to "config" or omitted since this is the default
#    value.  Note that the "ETag" and "Last-Modified" headers are only
#    returned if the content parameter value is "config".
#
#    GET /restconf/data/example-events:events?content=config
#        HTTP/1.1
#    Host: example.com
#    Accept: application/yang.data+json
#
#    The server might respond:
#
#       HTTP/1.1 200 OK
#       Date: Mon, 23 Apr 2012 17:11:30 GMT
#       Server: example-server
#       Last-Modified: Mon, 23 Apr 2012 13:01:20 GMT
#       ETag: eeeada438af
#       Cache-Control: no-cache
#       Pragma: no-cache
#       Content-Type: application/yang.data+json
#
#       {
#         "example-events:events" : {
#           "event" : [
#             {
#               "name" : "interface-up",
#               "description" : "Interface up notification count"
#             },
#             {
#               "name" : "interface-down",
#               "description" : "Interface down notification count"
#             }
#           ]
#         }
#       }
#
#    Example 3: content=nonconfig
#
#    To retrieve only the non-configuration child resources, the "content"
#    parameter is set to "nonconfig".  Note that configuration ancestors
#    (if any) and list key leafs (if any) are also returned.  The client
#    might send:
#
#    GET /restconf/data/example-events:events?content=nonconfig
#        HTTP/1.1
#    Host: example.com
#    Accept: application/yang.data+json
#
#    The server might respond:
#
#       HTTP/1.1 200 OK
#       Date: Mon, 23 Apr 2012 17:11:30 GMT
#       Server: example-server
#       Cache-Control: no-cache
#       Pragma: no-cache
#       Content-Type: application/yang.data+json
#
#       {
#         "example-events:events" : {
#           "event" : [
#             {
#               "name" : "interface-up",
#               "event-count" : 42
#             },
#             {
#               "name" : "interface-down",
#               "event-count" : 4
#             }
#           ]
#         }
#       }
#
# D.3.2.  "depth" Parameter
#
#    The "depth" parameter is used to limit the number of levels of child
#    resources that are returned by the server for a GET method request.
#
#    The depth parameter starts counting levels at the level of the target
#    resource that is specified, so that a depth level of "1" includes
#    just the target resource level itself.  A depth level of "2" includes
#    the target resource level and its child nodes.
#
#    This example shows how different values of the "depth" parameter
#    would affect the reply content for retrieval of the top-level
#    "jukebox" data resource.
#
#    Example 1: depth=unbounded
#
#    To retrieve all the child resources, the "depth" parameter is not
#    present or set to the default value "unbounded".  Note that some
#    strings are wrapped for display purposes only.
#
#    GET /restconf/data/example-jukebox:jukebox?depth=unbounded
#        HTTP/1.1
#    Host: example.com
#    Accept: application/yang.data+json
#
#    The server might respond:
#
#       HTTP/1.1 200 OK
#       Date: Mon, 23 Apr 2012 17:11:30 GMT
#       Server: example-server
#       Cache-Control: no-cache
#       Pragma: no-cache
#       Content-Type: application/yang.data+json
#
#       {
#         "example-jukebox:jukebox" : {
#           "library" : {
#             "artist" : [
#               {
#                 "name" : "Foo Fighters",
#                 "album" : [
#                   {
#                     "name" : "Wasting Light",
#                     "genre" : "example-jukebox:alternative",
#                     "year" : 2011,
#                     "song" : [
#                       {
#                         "name" : "Wasting Light",
#                         "location" :
#                           "/media/foo/a7/wasting-light.mp3",
#                         "format" : "MP3",
#                         "length" " 286
#                       },
#                       {
#                         "name" : "Rope",
#                         "location" : "/media/foo/a7/rope.mp3",
#                         "format" : "MP3",
#                         "length" " 259
#                       }
#                     ]
#                   }
#                 ]
#               }
#             ]
#           },
#           "playlist" : [
#             {
#               "name" : "Foo-One",
#               "description" : "example playlist 1",
#               "song" : [
#                 {
#                   "index" : 1,
#                   "id" : "https://example.com/restconf/data/
#                         example-jukebox:jukebox/library/artist=
#                         Foo%20Fighters/album=Wasting%20Light/
#                         song=Rope"
#                 },
#                 {
#                   "index" : 2,
#                   "id" : "https://example.com/restconf/data/
#                         example-jukebox:jukebox/library/artist=
#                         Foo%20Fighters/album=Wasting%20Light/song=
#                         Bridge%20Burning"
#                 }
#               ]
#             }
#           ],
#           "player" : {
#             "gap" : 0.5
#           }
#         }
#       }
#
#    Example 2: depth=1
#
#    To determine if 1 or more resource instances exist for a given target
#    resource, the value "1" is used.
#
#    GET /restconf/data/example-jukebox:jukebox?depth=1 HTTP/1.1
#    Host: example.com
#    Accept: application/yang.data+json
#
#    The server might respond:
#
#       HTTP/1.1 200 OK
#       Date: Mon, 23 Apr 2012 17:11:30 GMT
#       Server: example-server
#       Cache-Control: no-cache
#       Pragma: no-cache
#       Content-Type: application/yang.data+json
#       {
#         "example-jukebox:jukebox" : {}
#       }
#
#    Example 3: depth=3
#
#    To limit the depth level to the target resource plus 2 child resource
#    layers the value "3" is used.
#
#    GET /restconf/data/example-jukebox:jukebox?depth=3 HTTP/1.1
#    Host: example.com
#    Accept: application/yang.data+json
#
#    The server might respond:
#
#       HTTP/1.1 200 OK
#       Date: Mon, 23 Apr 2012 17:11:30 GMT
#       Server: example-server
#       Cache-Control: no-cache
#       Pragma: no-cache
#       Content-Type: application/yang.data+json
#
#       {
#         "example-jukebox:jukebox" : {
#           "library" : {
#             "artist" : {}
#           },
#           "playlist" : [
#             {
#               "name" : "Foo-One",
#               "description" : "example playlist 1",
#               "song" : {}
#             }
#           ],
#           "player" : {
#             "gap" : 0.5
#           }
#         }
#       }
#
# D.3.3.  "fields" Parameter
#
#    In this example the client is retrieving the API resource, but
#    retrieving only the "name" and "revision" nodes from each module, in
#    JSON format:
#
#    GET /restconf/data?fields=ietf-yang-library:modules/
#        module(name;revision) HTTP/1.1
#
#    Host: example.com
#    Accept: application/yang.data+json
#
#    The server might respond as follows.
#
#       HTTP/1.1 200 OK
#       Date: Mon, 23 Apr 2012 17:01:00 GMT
#       Server: example-server
#       Content-Type: application/yang.data+json
#
#       {
#         "ietf-yang-library:modules": {
#           "module": [
#             {
#               "name" : "example-jukebox",
#               "revision" : "2015-06-04"
#             },
#             {
#               "name" : "ietf-inet-types",
#               "revision" : "2013-07-15"
#             },
#             {
#               "name" : "ietf-restconf-monitoring",
#               "revision" : "2015-06-19"
#             },
#             {
#               "name" : "ietf-yang-library",
#               "revision" : "2016-02-01"
#             },
#             {
#               "name" : "ietf-yang-types",
#               "revision" : "2013-07-15"
#             }
#
#           ]
#         }
#       }
#
# D.3.4.  "insert" Parameter
#
#    In this example, a new first entry in the "Foo-One" playlist is being
#    created.
#
#    Request from client:
#
#       POST /restconf/data/example-jukebox:jukebox/
#           playlist=Foo-One?insert=first HTTP/1.1
#       Host: example.com
#       Content-Type: application/yang.data+json
#
#       {
#         "example-jukebox:song" : {
#            "index" : 1,
#            "id" : "/example-jukebox:jukebox/library/
#                artist=Foo%20Fighters/album=Wasting%20Light/song=Rope"
#          }
#       }
#
#    Response from server:
#
#    HTTP/1.1 201 Created
#    Date: Mon, 23 Apr 2012 13:01:20 GMT
#    Server: example-server
#    Last-Modified: Mon, 23 Apr 2012 13:01:20 GMT
#    Location: https://example.com/restconf/data/
#        example-jukebox:jukebox/playlist=Foo-One/song=1
#    ETag: eeeada438af
#
# D.3.5.  "point" Parameter
#
#    In this example, the client is inserting a new "song" resource within
#    an "album" resource after another song.  The request URI is split for
#    display purposes only.
#
#    Request from client:
#
#       POST /restconf/data/example-jukebox:jukebox/
#           library/artist=Foo%20Fighters/album=Wasting%20Light?
#           insert=after&point=%2Fexample-jukebox%3Ajukebox%2F
#           library%2Fartist%3DFoo%20Fighters%2Falbum%3D
#           Wasting%20Light%2Fsong%3DBridge%20Burning   HTTP/1.1
#       Host: example.com
#       Content-Type: application/yang.data+json
#
#       {
#         "example-jukebox:song" : {
#           "name" : "Rope",
#           "location" : "/media/foo/a7/rope.mp3",
#           "format" : "MP3",
#           "length" : 259
#         }
#       }
#
#    Response from server:
#
#    HTTP/1.1 204 No Content
#    Date: Mon, 23 Apr 2012 13:01:20 GMT
#    Server: example-server
#    Last-Modified: Mon, 23 Apr 2012 13:01:20 GMT
#    ETag: abcada438af
#
# D.3.6.  "filter" Parameter
#
#    The following URIs show some examples of notification filter
#    specifications (lines wrapped for display purposes only):
#
#       // filter = /event/event-class='fault'
#       GET /streams/NETCONF?filter=%2Fevent%2Fevent-class%3D'fault'
#
#       // filter = /event/severity<=4
#       GET /streams/NETCONF?filter=%2Fevent%2Fseverity%3C%3D4
#
#       // filter = /linkUp|/linkDown
#       GET /streams/SNMP?filter=%2FlinkUp%7C%2FlinkDown
#
#       // filter = /*/reporting-entity/card!='Ethernet0'
#       GET /streams/NETCONF?
#          filter=%2F*%2Freporting-entity%2Fcard%21%3D'Ethernet0'
#
#       // filter = /*/email-addr[contains(.,'company.com')]
#       GET /streams/critical-syslog?
#          filter=%2F*%2Femail-addr[contains(.%2C'company.com')]
#
#       // Note: the module name is used as prefix.
#       // filter = (/example-mod:event1/name='joe' and
#       //           /example-mod:event1/status='online')
#       GET /streams/NETCONF?
#         filter=(%2Fexample-mod%3Aevent1%2Fname%3D'joe'%20and
#                 %20%2Fexample-mod%3Aevent1%2Fstatus%3D'online')
#
#       // To get notifications from just two modules (e.g., m1 + m2)
#       // filter=(/m1:* or /m2:*)
#       GET /streams/NETCONF?filter=(%2Fm1%3A*%20or%20%2Fm2%3A*)
#
# D.3.7.  "start-time" Parameter
#
#    // start-time = 2014-10-25T10:02:00Z
#    GET /streams/NETCONF?start-time=2014-10-25T10%3A02%3A00Z
#
# D.3.8.  "stop-time" Parameter
#
#    // stop-time = 2014-10-25T12:31:00Z
#    GET /mystreams/NETCONF?stop-time=2014-10-25T12%3A31%3A00Z
#
# D.3.9.  "with-defaults" Parameter
#
#    The following YANG module is assumed for this example.
#
#      module example-interface {
#        prefix "exif";
#        namespace "urn:example.com:params:xml:ns:yang:example-interface";
#
#        container interfaces {
#          list interface {
#            key name;
#            leaf name { type string; }
#            leaf mtu { type uint32; }
#            leaf status {
#              config false;
#              type enumeration {
#                enum up;
#                enum down;
#                enum testing;
#              }
#            }
#          }
#        }
#      }
#
#    Assume the same data model as defined in Appendix A.1 of [RFC6243].
#    Assume the same data set as defined in Appendix A.2 of [RFC6243].  If
#    the server defaults-uri basic-mode is "trim", the the following
#    request for interface "eth1" might be as follows:
#
#    Without query parameter:
#
#    GET /restconf/data/example:interfaces/interface=eth1 HTTP/1.1
#    Host: example.com
#    Accept: application/yang.data+json
#
#    The server might respond as follows.
#
#       HTTP/1.1 200 OK
#       Date: Mon, 23 Apr 2012 17:01:00 GMT
#       Server: example-server
#       Content-Type: application/yang.data+json
#
#       {
#         "example:interface": [
#           {
#             "name" : "eth1",
#             "status" : "up"
#           }
#         ]
#       }
#
#    Note that the "mtu" leaf is missing because it is set to the default
#    "1500", and the server defaults handling basic-mode is "trim".
#
#    With query parameter:
#
#    GET /restconf/data/example:interfaces/interface=eth1
#        ?with-defaults=report-all HTTP/1.1
#    Host: example.com
#    Accept: application/yang.data+json
#
#    The server might respond as follows.
#
#       HTTP/1.1 200 OK
#       Date: Mon, 23 Apr 2012 17:01:00 GMT
#       Server: example-server
#       Content-Type: application/yang.data+json
#
#       {
#         "example:interface": [
#           {
#             "name" : "eth1",
#             "mtu" : 1500,
#             "status" : "up"
#           }
#         ]
#       }
#
#    Note that the server returns the "mtu" leaf because the "report-all"
#    mode was requested with the "with-defaults" query parameter.
#
#
#
