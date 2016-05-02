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
import string
import urllib


class RestconfDataResource(object):
    """
    This class wraps a RESTCONF data resource string and allows for paths and module information
    to be easily extracted.

    This class checks for simple errors and does not test validity against an existing model
    """
    _resource_dict = {}
    _valid = True
    _error_message = ''
    # _badStart = 'XxMmLl'      # TODO The MUST NOT start clause seems incorrect?
    _badStart = ''
    _goodStart = (string.ascii_letters + '_').translate(None, ''.join(_badStart))
    _validChars = string.ascii_letters + string.digits + '_-.'
    _invalidChars = string.printable.translate(None, ''.join(_validChars))
    _percentEncoded = urllib.quote(',:" /') + urllib.quote("'")

    #   An identifier MUST NOT start with ((X|x) (M|m) (L|l))

    def __init__(self, resource):
        self._resource = resource
        self._parse_api_path(resource)

    @staticmethod
    def valid_identifier(identifier):
        """
        #   An identifier MUST NOT start with ((X|x) (M|m) (L|l))
        #
        #           identifier = (ALPHA / "_") *(ALPHA / DIGIT / "_" / "-" / ".")
        """
        return len(identifier) > 0 and \
               identifier[0] in RestconfDataResource._goodStart and \
               len(identifier.translate(None, RestconfDataResource._validChars)) == 0

    def _parse_api_path(self, resource):
        # api-path = "/" |
        #           ("/" api-identifier
        #           0*("/" (api-identifier | list-instance )))
        #
        #           api-identifier = [module-name ":"] identifier                 ;; note 1
        #
        #           module-name = identifier
        #
        #           list-instance = api-identifier "=" key-value ["," key-value]*
        #
        #           key-value = string                                            ;; note 1
        #
        #           string = <a quoted or unquoted string>
        #
        #   An identifier MUST NOT start with ((X|x) (M|m) (L|l))
        #
        #           identifier = (ALPHA / "_") *(ALPHA / DIGIT / "_" / "-" / ".")
        #
        # Note 1: The syntax for "api-identifier" and "key-value" MUST conform to the
        #         JSON identifier encoding rules in Section 4 of [I-D.ietf-netmod-yang-json]

        api_identifier_list = resource.split('/')
        module_name = ''

        for api_identifier in api_identifier_list:
            # New module entry if a ':" is encountered

            if api_identifier.contains(':'):
                # Should only have a single ':', so the list size should be two

                module_and_identifier = api_identifier.split(':')

                if len(module_and_identifier) == 2:
                    module_name = module_and_identifier[0]
                    status, module_name, identifier = self._parse_module_and_identifier(module_name,
                                                                                        module_and_identifier[1])
                else:
                    self._error_message = "Invalid Module and Identity '%s' found in resource path: '%s'" % \
                                          (api_identifier, self._resource)
                    self._valid = False
                    break
            else:
                status, module_name, identifier = self._parse_identifier_or_list_instance(api_identifier,
                                                                                          module_name)
            if not status:
                self._valid = False
                break

            # Add new module name entry if needed

            if module_name not in self._resource_dict:
                self._resource_dict[module_name] = []

            self._resource_dict[module_name].extend(identifier)

    def _parse_module_and_identifier(self, module_name, identifier):
        """
        Process a api-identifier that is made up of a module and an identifier.  This
        is the case where

            api-identifier = [module-name ":"] identifier
        and
            module-name = identifier

        and the 'module-name' was located in the api-identifier

        :param module_name: (string) The module-name
        :param identifier: (string) The identifier

        :returns: (boolean) True if successfully parsed
        """

        if not RestconfDataResource.valid_identifier(module_name):
            self._error_message = "Invalid Module '%s' found in resource path: '%s'" % \
                                  (module_name, self._resource)
            return False, None, None

        # Parse the identifier now

        return self._parse_identifier_or_list_instance(module_name, identifier)

    def _parse_identifier_or_list_instance(self, current_module_name, identifier):
        """
        Process a api-identifier that is made up of an identifier.  This is the case where:

            api-identifier = [module-name ":"] identifier

        and the 'module-name' was NOT located in the api-identifier
        and
            list-instance = api-identifier "=" key-value ["," key-value]*

        :param current_module_name: (string) The module-name
        :param identifier: (string) The identifier

        :returns: (boolean) True if successfully parsed.
        """
        # This is either an identifier or a list-instance.  List-instances will always contain
        # and "=" since it is not a valid instance character

        if '=' in identifier:
            return self._parse_list_instance(current_module_name, identifier)

        if not RestconfDataResource.valid_identifier(identifier):
            self._error_message = "Invalid Identifier '%s' found in resource path: '%s'" % \
                                  (identifier, self._resource)
            return False, None, None

        return True, current_module_name, identifier

    def _parse_list_instance(self, current_module_name, list_instance):
        """
        Process the list-instance portion of an api-identifier where:

            list-instance = api-identifier "=" key-value ["," key-value]*

               key-value = string

               string = <a quoted or unquoted string>

        :param current_module_name: (string) The module-name
        :param list_instance: (string) The identifier

        :returns: (boolean) True if successfully parsed.
        """
        # This is either an identifier or a list-instance.  List-instances will always contain
        # and "=" since it is not a valid instance character

        instance_and_keys = list_instance.split('=')

        if len(instance_and_keys) != 2 or len(instance_and_keys[1].strip()) == 0:
            self._error_message = "Invalid list-instance '%s' found in resource path: '%s'" % \
                                  (list_instance, self._resource)
            return False, None, None

        identifier = instance_and_keys[0]

        if not RestconfDataResource.valid_identifier(identifier):
            self._error_message = "Invalid Identifier '%s' found in resource path: '%s'" % \
                                  (identifier, self._resource)
            return False, None, None

        # TODO: Is there a better way to encode keys
        identifier += '[%s]' % instance_and_keys[1].strip()

        return True, current_module_name, identifier

    @property
    def dict(self):
        return self._resource_dict

    @property
    def is_valid(self):
        return self._valid

    @property
    def error_message(self):
        return self._error_message

    def __str__(self):
        return self._resource
