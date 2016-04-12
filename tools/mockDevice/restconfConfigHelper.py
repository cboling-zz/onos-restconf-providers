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
from datetime import datetime
from uuid import uuid4


class RestconfConfigHelper(object):
    """
    Provides RESTCONF required properties/capabilities for each node in a YANG data model
    that is a configuration data resource.

    A RESTCONF server MUST maintain a last-modified timestamp and an Entity Tag (ETag) for
    the top-level {+restconf}/data resource and SHOULD maintain them for other Configuration
    data resources.
    """
    lastModifiedTimestamp = datetime.utcnow()
    eTag = str(uuid4())
    parent = None

    def __init__(self, parent=None):
        """
        :param parent: (restconfConfigHelper) The first ancestor of this configuration node
        """
        # TODO: Look into YANG specification and see if there are any other options/params we may want to pass in
        self.parent = parent

    def get_last_modified_timestamp(self, *args, **kwargs):
        """
        Provides the last change time (used in "Last-Modified" header) for this resource.

        This timestamp is only affected by configuration data resources, and MUST NOT be
        updated for changes to non-configuration data.

        :return: (datetime) the UTC timestamp that this tree was last modified
        """
        return self.lastModifiedTimestamp

    def set_modified(self, *args, **kwargs):
        """
        Update the last modified time to 'now'

        This timestamp is only affected by configuration data resources, and MUST NOT be
        updated for changes to non-configuration data.

        :param updateTime: (dateTime) Optional argument that specifies the update time. This is often
                                      used when recursing up the ancestor list.
        """
        self.lastModifiedTimestamp = kwargs.get('updateTime', datetime.utcnow())
        self.eTag = str(uuid4())  # update the eTag

        # Any change of a configuration item requires update of any ancestor data resources as well

        if self.parent is not None:
            self.parent.set_modified(updateTime=self.lastModifiedTimestamp)

    def get_entity_tag(self, *args, **kwargs):
        """
        Provides the entity tag (used by the "If-Match" header) for this resource.

        This entity tag is only affected by configuration data resources, and MUST NOT be
        updated for changes to non-configuration data.

        :return: (string) unique opaque string
        """
        return self.eTag
