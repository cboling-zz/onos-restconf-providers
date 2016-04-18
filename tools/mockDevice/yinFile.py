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
import xml.etree.ElementTree
from xml.etree.ElementTree import QName
from pyangbind.lib.base import PybindBase
from pyangbind.lib.yangtypes import YANGDynClass
from pyangbind.lib.yangtypes import YANGListType, TypedListType
import pprint
import datetime


class YINFile:
    """
    Class to support reading and parsing YIN file
    """
    _namespace = None  # The XML namespace for this file

    # The following YANG keywords are marked with 'name' in the YIN file and are important
    # to us. Note that to search for them, you will need to prepend any namespace.  Note that
    # we really only care about supporting a set of Simple YANG models with this class since
    # it is being used to create test RESTCONF servers for unit testing of the RESTCONF SB.

    _important_keywords = ['container',
                           'list',
                           'leaf',
                           'leaf-list',
                           'choice',
                           'anyxml',
                           'uses',  # TODO: Investigate how this and grouping appear in YIN and not
                           # that it could use 'refine' and change the 'config' value
                           ]

    def __init__(self, file_path):
        """
        Initializer

        :param file_path: (string) Path to YIN file
        """
        self._path = file_path
        self._root = xml.etree.ElementTree.parse(file_path).getroot()
        if self.root.tag[0] == "{":
            self._namespace, _ignore1, _ignore2 = self.root.tag[1:].partition("}")

        self._keywords = [self.get_name_with_namespace(kw) for kw in self._important_keywords]

        pass  # Verify keywords above
        # if self.root.tag[0] == "{":
        #     self.namespace, _ignore1, _ignore2 = self.root.tag[1:].partition("}")
        #     container_tag = str(QName(self.namespace, 'container'))
        # else:
        #     container_tag = 'container'
        #
        # self.containers = self.root.findall(container_tag)


    @property
    def file_path(self):
        """
        The file path related to this object

        :returns: (string) YIN file path
        """
        return self._path

    @property
    def module_name(self):
        """
        :returns: (string) The module name for this model.  None returned if not found
        """
        try:
            return self._root.attrib['name']
        except KeyError:
            return None

    @property
    def namespace(self):
        """
        :returns: (string) The XML namespace for the file
        """
        return self._namespace

    def get_name_with_namespace(self, name):
        """
        Extracts the simple name of an item without the namespace

        :param name: (string) Short element name

        :returns: (string) Name wit the namespace (if any)

        """
        return name if self._namespace is None else str(QName(self.namespace, name))

    def get_name_wo_namespace(self, fullname):
        """
        Extracts the simple name of an item without the namespace

        :param fullname: (string) Namespace + an element name

        :returns: (string) Name without the namespace

        """
        return fullname if self._namespace is None else fullname.replace('{%s}' % self._namespace, '')

    def is_config(self, element, include_children=False):
        """
        Is an element, and optionally any children, are config-true

        :returns: (boolean) True if the element has config-data 'true' properties
        """
        pass

    @property
    def module_revision(self):
        """
        Returns the latest editorial revision number for the module.  RFC 6020 specifies that
        a module SHOULD include the revision history and SHOULD have the latest one at the front

        :returns: (datetime) revision history in "YYYY-MM-DD" format or None if not found
        """
        rev_list = self._root.findall(self.get_name_with_namespace('revision'))

        if rev_list is None or len(rev_list) == 0:
            return None

        # Return the revision number
        return datetime.datetime.strptime('%Y-%m-%d', rev_list[0].attrib['date']) \
            if 'date' in rev_list[0].attrib else None

    def get_extmethods(self, value, node=None, path_base=''):
        """
        A recursive function to convert a yang model into a extmethods dictionary

        :param value: (dict) Child elements (YANGBaseClass or more dict) of a the model instance
        :param path_base: (dict) The pyangbind extmethods base path for this value/node
        :param node: (ElementTree element) The XML element in the YIN file that corresponds to the
                                           value parameter

        :returns: (dict) A pyangbind compatible extmethods dictionary
        """
        extmethods = {}

        # Processes only dictionaries.

        if value is None or not isinstance(value, dict):
            return extmethods

        # if 'node' is None, then this is the first time we have been called. The 'self._root' variable
        # points to the XML root 'module'.

        if node is None:
            node = self._root

        for key, item in value.items():
            # Calculate extmethods 'path' for this item

            path = path_base + '/' + key

            item_node = self._root.find('./*[@%s]' % key)
            config = True

            # root.findall('./*[@name]')   Returns all children with a 'name' attribute
            # root.findall('./*[@name]')[0]  First matching child
            # root.findall('./*[@name]')[0].tag    -> first child tag such as string '{urn:ietf:params:xml:ns:yang:yin:1}identity'
            # root.findall('./*[@name]')[0].attrib -> first child attribute value such as dict {'name': 'genre'}

            # keywords = ['{urn:ietf:params:xml:ns:yang:yin:1}container','{urn:ietf:params:xml:ns:yang:yin:1}list','{urn:ietf:params:xml:ns:yang:yin:1}leaf']
            # xyz = [ x for x in root.findall('./*[@name]') if x.tag in keywords ]
            # xyz is a list of all children who have a name attribute and the tag is the namespace+keyword value

            # key = 'jukebox'
            # abc = [ x for x in root.findall('./*[@name]') if x.tag in keywords and x.attrib['name'] == key ]
            # print abc
            # [<Element '{urn:ietf:params:xml:ns:yang:yin:1}container' at 0x7f3b41cb0810>]

            # _important_keywords

            # self.get_name_wo_namespace()

            # NOTES:
            # For containers, a 'presence'  is explicitly for config
            #
            # yang_name = getattr(val, "yang_name") if hasattr(value, "yang_name") else None
            # is_container = hasattr(val, "get")

            try:
                if item._is_leaf:  # Protected, but I really need to know
                    config = item.flags.writeable

            except AttributeError:
                pass  # Was another dictionary item or did not have a writeable flag

            # Add this to our path
            extmethods[path] = config
            extmethods.update(self.get_extmethods(value=item, node=node, path_base=path))

        return extmethods

        # Special processing notes on determining types and characteristics we might want to exploit:
        #
        # If 'container' then the 'presense' statement indicates that the container itself is for configuration data.
        #    so if not found, we will need to look into the children to see if any of them are NOT config-false.
        #    A container can also have the 'config' value present
        #
        # Default 'config' choice is true. Once 'config' is false, all children are considered 'config' false
