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

from urlparse import urlparse

from restconfUrl import RestconfUrl


class RestconfLibraryUrl(RestconfUrl):
    """
    Operations API Resource URL Parse wrapper for RESTCONF

    This class is responsible for validating RESTCONF URL syntax according to
    draft-10 rules
    """

    def __init__(self, url, method='GET', api_root='restconf'):
        RestconfUrl.__init__(self, url, method=method, api_root=api_root)

    def resource_api(self):
        return RestconfUrl.LIBRARY_RESOURCE_API
