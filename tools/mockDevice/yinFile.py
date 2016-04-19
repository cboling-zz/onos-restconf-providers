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
import datetime
from restconfConfigHelper import RestconfConfigHelper
from restconfStatusHelper import RestconfStatusHelper


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

    def __init__(self, file_path, verbose=False):
        """
        Initializer

        :param file_path: (string) Path to YIN file
        :param: verbose (integer) Flag indicating if verbose output is to be presented
        """
        self._path = file_path
        self._verbose = verbose

        self._root = xml.etree.ElementTree.parse(file_path).getroot()  # Locate the 'module' root node

        if self._root.tag[0] == "{":
            self._namespace, _ignore1, _ignore2 = self._root.tag[1:].partition("}")

        self._keywords = [self.get_name_with_namespace(kw) for kw in self._important_keywords]

    def __str__(self):
        return 'YINFile: %s' % self.file_path

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

    def get_extmethods(self, value, node=None, path_base='', parent_helper=None):
        """
        A recursive function to convert a yang model into a extmethods dictionary

        :param value: (dict) Child elements (YANGBaseClass or more dict) of a the model instance
        :param path_base: (dict) The pyangbind extmethods base path for this value/node
        :param node: (ElementTree element) The XML element in the YIN file that corresponds to the
                                           value parameter
        :param parent_helper: (restconfDataHelper) Parent RESTCONF data helper object


        restconfConfigHelper
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

            # Get the associated YIN node.  Should match only one
            # TODO: Change to just a 'find' if it holds true we only find one

            node_list = [n for n in node.findall('./*[@name]')
                         if n.tag in self._keywords and n.attrib['name'] == key
                         ]

            if len(node_list) == 0:
                # TODO should this be an error?
                continue

            if len(node_list) > 1:
                # TODO should this be an error?
                print('node list is greater than one')

            key_node = node_list[0]
            config = parent_helper is None or parent_helper.is_config

            # If config is true for ancestor, see if it is true for this node as well

            if config:
                config_node = key_node.find('./%s' % self.get_name_with_namespace('config'))
                config = config_node is None or config_node.attrib['value'].lower() != 'false'

            helper = RestconfConfigHelper(key_node, parent_helper) if config \
                else RestconfStatusHelper(key_node, parent_helper)

            extmethods[path] = helper

            if self._verbose > 0:
                print 'Node %s is%s a config node' % (self.get_name_wo_namespace(key_node.tag),
                                                      '' if config else ' not')
            # Recurse and add to list

            extmethods.update(self.get_extmethods(value=item, node=key_node, path_base=path, parent_helper=helper))

        return extmethods

