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


class Request(object):
    """
    Base class implementation for RESTCONF request (client->server) support
    """

    ###########################################################################
    # Query Parameters (section 4.8 of draft 10)
    #
    #   Each RESTCONF operation allows zero or more query parameters to be
    #   present in the request URI. The specific parameters that are allowed
    #   depends on the resource type, and sometimes the specific target
    #   resource used, in the request

    @property
    def content(self):
        pass  # TODO: Implement this

    @content.setter
    def content(self, value):
        pass  # TODO: Implement this
