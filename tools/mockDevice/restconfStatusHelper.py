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
from datetime import datetime
from uuid import uuid4
from restconfDataHelper import RestconfDataHelper


class RestconfStatusHelper(RestconfDataHelper):
    """
    Provides RESTCONF required properties/capabilities for each node in a YANG data model
    that is a status (non-configuration) data resource.
    """

    def __init__(self, node, parent=None):
        """
        :param node: (ElementTree Element) The YIN node for this node
        :param parent: (restconfConfigHelper) The first ancestor of this configuration node
        """
        RestconfDataHelper.__init__(self, node, parent=parent)
        # TODO: Look into YANG specification and see if there are any other options/params we may want to pass in

    def __str__(self):
        return 'RestconfStatusHelper: %s' % self.yin_node.attrib['name']

        # TODO Use base class and delete this if we never add to it
