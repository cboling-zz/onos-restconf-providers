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


class RestconfDataHelper(object):
    """
    Provides base RESTCONF required properties/capabilities for each node in a YANG data model
    that is a common to configuration and non-configuration data resources ...
    """
    parent = None
    isContainer = False

    def __init__(self, parent=None):
        """
        :param parent: (RestconfHelper) The first ancestor of this node
        """
        # TODO: Look into YANG specification and see if there are any other options/params we may want to pass in
        self.parent = parent

    @property
    def is_config(self):
        """
        :returns: (Boolean) True if this item is configurable
        """
        return False

    @property
    def is_container(self):
        """
        :returns: (Boolean) True if this item is a container of other items
        """
        return self.isContainer
