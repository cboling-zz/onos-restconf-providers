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
        self._parse_resource(resource)

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

    def _parse_resource(self, resource):
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

                if len(module_and_identifier) != 2:
                    self._error_message = "Invalid Module and Identity '%s' found in resource path: '%s'" % \
                                          (api_identifier, self._resource)
                    self._valid = False
                    break

                # Extract module and identifier

                module_name = module_and_identifier[0]

                if not RestconfDataResource.valid_identifier(module_name):
                    self._error_message = "Invalid Module '%s' found in resource path: '%s'" % \
                                          (module_name, self._resource)
                    self._valid = False
                    break

                identifier = module_and_identifier[1]

                if not RestconfDataResource.valid_identifier(identifier):
                    self._error_message = "Invalid Identifier '%s' found in resource path: '%s'" % \
                                          (identifier, self._resource)
                    self._valid = False
                    break

            # Add new module name entry if needed

            if module_name not in self._resource_dict:
                self._resource_dict[module_name] = []

            # TODO start here Saturday.  need to populate dictionary entry with the path...

            self._resource_dict[module_name].extend(identifier)


            # TODO: Enforce 'Note 1' validation

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
