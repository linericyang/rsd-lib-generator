# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import os
from packaging import version
import re
import json
import pprint
import sys
import subprocess

import untangle
import jinja2


XML_DIR = '/Users/lyang28/workspace/github/intelRSD/PODM/SW/pod-manager/'\
          'podm-rest/src/main/resources'
SCHEMA_DB = {}
NEED_SUSHY_BASE = False
NEED_SUSHY_UTILS = False
NEED_RSD_LIB_UTILS = False


def wrap_resource_description(des):
    if des is None:
        return None

    s = des.strip().rstrip()
    if len(s) <= 72:
        return ' '*7 + des + '\n    """'

    l = [' '*7]
    while len(s) > 72:
        index = s.rfind(" ", 0, 72)
        l.append(s[:index]+'\n'+" "*7)
        s = s[index:]
        s = s.strip().rstrip()

    l.append(s+"\n")
    l.append('    """')

    return "".join(l)

def wrap_field_description(des):
    if des is None:
        return None

    s = des.strip().rstrip()
    if len(s) <= 69:
        return ' '*4 + '"""' + s + '"""'

    l = ['    """']
    while len(s) > 72:
        index = s.rfind(" ", 0, 72)
        l.append(s[:index]+'\n'+" "*7)
        s = s[index:]
        s = s.strip().rstrip()

    l.append(s+"\n")
    l.append('    """')

    return "".join(l)

def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError

def camelcase_to_underscore_joined(camelcase_str):
    """Convert camelCase string to underscore_joined string

    :param camelcase_str: The camelCase string
    :returns: the equivalent underscore_joined string
    """
    if not camelcase_str:
        raise ValueError('"camelcase_str" cannot be empty')

    r = camelcase_str[0].lower()
    for i, letter in enumerate(camelcase_str[1:], 1):
        if letter.isupper():
            try:
                if (camelcase_str[i - 1].islower()
                        or camelcase_str[i + 1].islower()):
                    r += '_'
            except IndexError:
                pass

        r += letter.lower()

    return r

def prepare_schemas():
    for xml in os.listdir(XML_DIR):
        doc = untangle.parse(os.path.join(XML_DIR, xml))

        for schema in doc.edmx_Edmx.edmx_DataServices.Schema:
            SCHEMA_DB[schema['Namespace']] = schema

    return SCHEMA_DB

def split_version(namespace):
    result = namespace.split('.')
    if len(result) == 2:
        return result[0], version.parse(result[1])
    elif len(result) == 1:
        return result[0], version.parse('v0_0_0')

def find_latest_namespace(module_name):
    all_namespaces = SCHEMA_DB.keys()
    latest_namespace = None
    latest_version = None

    for namespace in all_namespaces:
        regex = '(^{namespace}$|^{namespace}\.v)'.format(namespace=module_name)
        if re.search(regex, namespace):
            _, version = split_version(namespace)

            if latest_namespace is None:
                latest_namespace = namespace
                latest_version = version
            elif version > latest_version:
                latest_namespace = namespace
                latest_version = version

    return latest_namespace

def get_description(element):
    for annot in getattr(element, "Annotation", []):
        if annot['Term'] == "OData.Description":
                return  annot['String']
    return None

def is_reference(element):
    for annot in getattr(element, "Annotation", []):
        if annot['Term'] == "OData.AutoExpandReferences":
                return  True
    return False

def get_resource(namespace, name):
    element = get_entity(namespace, name)

    resource = {
        'Name': element['Name'],
        'Namespace': namespace,
        'ModuleName': name,
        'ElementType': element._name,
        'BaseType': element['BaseType'],
        'IsReferenceableMember': False,
        'Description': wrap_resource_description(get_description(element)),
        'Properties': {}
    }

    for i in getattr(element, "Property", []):
        if i['Type'].startswith("Collection("):
            t = i['Type'][len("Collection("):-1]
        else:
            t = i['Type']
        namespace, module_name = split_namespace(t)
        p = {
            'Name': i['Name'],
            'Type': i['Type'],
            'Description': wrap_field_description(get_description(i)),
            'IsReferences': is_reference(i),
            'IsCollection': i['Type'].startswith("Collection("),
            'Namespace': namespace,
            'ModuleName': module_name
        }

        resource['Properties'][i['Name']] = p

    for i in getattr(element, "NavigationProperty", []):
        if i['Type'].startswith("Collection("):
            t = i['Type'][len("Collection("):-1]
        else:
            t = i['Type']
        namespace, module_name = split_namespace(t)
        p = {
            'Name': i['Name'],
            'Type': i['Type'],
            'Description': wrap_field_description(get_description(i)),
            'IsReferences': is_reference(i),
            'IsCollection': i['Type'].startswith("Collection("),
            'Namespace': namespace,
            'ModuleName': module_name
        }

        resource['Properties'][i['Name']] = p

    return resource

def get_entity(namespace, name):
    # print(namespace, name)
    schema = SCHEMA_DB[namespace]
    for i in schema.children:
        if i['Name'] == name:
            return i
    return None

def split_namespace(type_str):
    index = type_str.rfind('.')
    return type_str[:index], type_str[index+1:]

def expand_generic_resource(resource):
    if resource['BaseType'] is None:
        return

    base_type = resource['BaseType']
    namespace, module_name = split_namespace(base_type)

    if base_type == "Resource.v1_0_0.ReferenceableMember":
        resource['IsReferenceableMember'] = True

    if namespace.startswith('Resource'):
        return

    sub_resource = get_resource(namespace, module_name)

    expand_generic_resource(sub_resource)

    if resource['Description'] is None:
        resource['Description'] = sub_resource['Description']
    if sub_resource["IsReferenceableMember"] == True:
        resource['IsReferenceableMember'] = True

    for k, v in resource['Properties'].items():
        sub_resource['Properties'][k] = v
    resource['Properties'] = sub_resource['Properties']

    # for k, v in resource['NavigationProperties'].items():
    #     sub_resource['NavigationProperties'][k] = v
    # resource['NavigationProperties'] = sub_resource['NavigationProperties']

    return

def find_latest_item_in_resource(module_name, item_name):
    all_namespaces = SCHEMA_DB.keys()
    latest_namespace = None
    latest_version = None

    for namespace in all_namespaces:
        regex = '(^{namespace}$|^{namespace}\.v)'.format(namespace=module_name)
        if re.search(regex, namespace):
            element = get_entity(namespace, item_name)
            _, version = split_version(namespace)

            if element is not None:
                if latest_namespace is None:
                    latest_namespace = namespace
                    latest_version = version
                elif version > latest_version:
                    latest_namespace = namespace
                    latest_version = version

    return '.'.join([latest_namespace, item_name])

def get_rsd_resource(namespace, resource_name):
    resource = get_resource(namespace, resource_name)

    expand_generic_resource(resource)

    return resource

def is_enumtype_or_typedefinition(resource_name):
    namespace, module_name = split_namespace(resource_name)
    resource = get_resource(namespace, module_name)

    if resource['ElementType'] == 'EnumType' or resource['ElementType'] == 'TypeDefinition':
        return True
    else:
        return False

def _prepare_render_properties(
    resource, global_resource_name, fields_name_set, fields_name_set_finished,
    collection_fields_name_set, collection_fields_name_set_finished,
    links_fields, other_modules, is_sub_resource=False):

    global NEED_SUSHY_BASE, NEED_SUSHY_UTILS, NEED_RSD_LIB_UTILS

    remove_key = []

    for key, value in resource['Properties'].items():
        value['PythonVariableName'] = camelcase_to_underscore_joined(value['Name'])

        value['IsSubResource'] = is_sub_resource

        if value["Name"] == "Actions":
            resource["HaveAction"] = True
            continue

        property_type = value['Type']

        if value['IsReferences'] == True:
            if resource["Name"] != "Links" and value['IsSubResource'] == False:
                if value["ModuleName"].endswith("Collection"):
                    value["PythonModuleName"] = camelcase_to_underscore_joined(value["ModuleName"][:len(value["ModuleName"])-10])
                else:
                    value["PythonModuleName"] = camelcase_to_underscore_joined(value["ModuleName"])
                links_fields.append(resource['Properties'][key])
                remove_key.append(key)
                if value['IsCollection'] == True:
                    NEED_RSD_LIB_UTILS = True
                else:
                    NEED_SUSHY_UTILS = True
            else:
                if value['IsCollection']:
                    value['Expression'] = 'base.Field("{0}", adapter=utils.get_members_identities)'.format(key)
                    NEED_SUSHY_UTILS = True
                    NEED_SUSHY_BASE = True
                else:
                    value['Expression'] = 'base.Field("{0}", adapter=rsd_lib_utils.get_resource_identity)'.format(key)
                    NEED_RSD_LIB_UTILS = True
                    NEED_SUSHY_BASE = True
        else:
            if property_type == "Edm.Int64" or property_type == "Edm.Decimal" or \
                property_type == "Edm.Int16" or property_type == "Edm.Int32" or \
                property_type == "Edm.Int64" or property_type == "Edm.SByte":
                value['Expression'] = 'base.Field("{0}", adapter=rsd_lib_utils.num_or_none)'.format(key)
                NEED_RSD_LIB_UTILS = True
            elif property_type == "Edm.Boolean":
                value['Expression'] = 'base.Field("{0}", adapter=bool)'.format(key)
                NEED_SUSHY_BASE = True
            elif property_type.startswith("Edm."):
                value['Expression'] = 'base.Field("{0}")'.format(key)
                NEED_SUSHY_BASE = True
            elif property_type == "Resource.UUID":
                value['Expression'] = 'base.Field("{0}")'.format(key)
                NEED_SUSHY_BASE = True
            elif property_type == "Resource.Status":
                value['Expression'] = 'rsd_lib_base.StatusField("{0}")'.format(key)
                if value['Description'] is None:
                    value['Description'] = wrap_field_description("This indicates the known state of the resource, such as if it is enabled.")
            elif property_type == "Resource.v1_1_0.Location":
                value['Expression'] = 'rsd_lib_base.LocationField("{0}")'.format(key)
            elif property_type == "Resource.v1_1_0.Identifier":
                value['Expression'] = 'rsd_lib_base.IdentifierField("{0}")'.format(key)
            elif property_type.startswith("Collection("):
                t = property_type[len("Collection("):-1]
                if t in ["Edm.String", "Edm.Int64", "Edm.Boolean"] or is_enumtype_or_typedefinition(t):
                    value['Expression'] = 'base.Field("{0}")'.format(key)
                else:
                    n, module_name = split_namespace(t)
                    namespace, version = split_version(n)
                    print("1"*10)
                    print(resource['Name'], value['Name'], property_type)
                    if namespace == global_resource_name or n == "Intel.Oem":
                        if namespace == global_resource_name:
                            t = find_latest_item_in_resource(namespace, module_name)
                        value['Expression'] = '{0}CollectionField("{1}")'.format(module_name, key)
                    else:
                        name = camelcase_to_underscore_joined(namespace)
                        value['Expression'] = '{0}.{1}CollectionField("{2}")'.format(name, module_name, key)
                        if name not in other_modules:
                            print("other module collection")
                            print(resource['Name'], value['Name'], property_type)
                            other_modules.append(name)
                    if t not in collection_fields_name_set_finished:
                        collection_fields_name_set.add(t)
            else:
                if is_enumtype_or_typedefinition(property_type):
                    value['Expression'] = 'base.Field("{0}")'.format(key)
                else:
                    n, module_name = split_namespace(property_type)
                    namespace, version = split_version(n)
                    print("2"*10)
                    print(resource['Name'], value['Name'], property_type)
                    if namespace == global_resource_name or n == "Intel.Oem":
                        if namespace == global_resource_name:
                            property_type = find_latest_item_in_resource(namespace, module_name)
                        value['Expression'] = '{0}Field("{1}")'.format(module_name, key)
                    else:
                        name = camelcase_to_underscore_joined(namespace)
                        value['Expression'] = '{0}.{1}Field("{2}")'.format(name, module_name, key)
                        if name not in other_modules:
                            print("other module")
                            print(resource['Name'], value['Name'], property_type)
                            other_modules.append(name)
                    if property_type not in fields_name_set_finished:
                        fields_name_set.add(property_type)

    for key in remove_key:
        resource['Properties'].pop(key)

def add_intel_oem_properties(resource):
    if not get_entity("Intel.Oem", resource['Name']):
        return

    resource["Properties"].update(
        {"Oem": {
            "Name": "Oem",
            "Description": wrap_field_description("Oem specific properties."),
            "PythonVariableName": "oem",
            "Expression": "OemField(\"Oem\")"
        }})
    resource['fields'].append(
        {
            "Name": "Oem",
            "ModuleName": "Oem",
            "Description": None,
            "Properties": {
                "Intel_RackScale": {
                    "Name": "Intel_RackScale",
                    "Description": wrap_field_description("Intel Rack Scale Design specific properties."),
                    "PythonVariableName": "intel_rackscale",
                    "Expression": "IntelRackScaleField(\"Intel_RackScale\")"
                }
            },
            'NavigationProperties': {}
        })
    resource['fields_name'].add(".".join(["Intel.Oem", resource['Name']]))

def prepare_render_resource(resource):
    resource['fields_name'] = set()
    resource['fields_name_finished'] = set()
    resource['fields'] = []
    resource['other_fields'] = []

    resource['collection_fields_name'] = set()
    resource['collection_fields_name_finished'] = set()
    resource['collection_fields'] = []
    resource['other_collection_fields'] = []

    resource['links_fields'] = []

    resource['other_modules'] = []

    _prepare_render_properties(
        resource, resource['Name'], resource['fields_name'],
        resource['fields_name_finished'],
        resource['collection_fields_name'],
        resource['collection_fields_name_finished'],
        resource['links_fields'],
        resource['other_modules'])

    add_intel_oem_properties(resource)

    while (len(resource['fields_name']) > 0 or len(resource['collection_fields_name']) > 0):
        if len(resource['fields_name']) > 0:
            field_type = resource['fields_name'].pop()
            if field_type not in resource['fields_name_finished']:
                resource['fields_name_finished'].add(field_type)
                print("Processing ", field_type)
                namespace, module_name = split_namespace(field_type)

                field = get_rsd_resource(namespace, module_name)
                _prepare_render_properties(
                    field, resource['Name'], resource['fields_name'],
                    resource['fields_name_finished'],
                    resource['collection_fields_name'],
                    resource['collection_fields_name_finished'],
                    resource['links_fields'], resource['other_modules'], True)

                if field['BaseType'] == "Resource.OemObject":
                    field['ModuleName'] = "IntelRackScale"

                if field_type.startswith(resource['Name']) or field_type.startswith("Intel.Oem"):
                    resource['fields'] = [field] + resource['fields']
                else:
                    resource['other_fields'] = [field] + resource['other_fields']

        if len(resource['collection_fields_name']) > 0:
            field_type = resource['collection_fields_name'].pop()
            if field_type not in resource['collection_fields_name_finished']:
                resource['collection_fields_name_finished'].add(field_type)
                namespace, module_name = split_namespace(field_type)

                field = get_rsd_resource(namespace, module_name)
                _prepare_render_properties(
                    field, resource['Name'], resource['fields_name'],
                    resource['fields_name_finished'],
                    resource['collection_fields_name'],
                    resource['collection_fields_name_finished'],
                    resource['links_fields'], resource['other_modules'], True)

                if field['BaseType'] == "Resource.OemObject":
                    field['ModuleName'] = "IntelRackScale"

                if field_type.startswith(resource['Name']) or field_type.startswith("Intel.Oem"):
                    resource['collection_fields'] = [field] + resource['collection_fields']
                else:
                    resource['other_collection_fields'] = [field] + resource['other_collection_fields']

    #Check whether Collection exist
    collection_name = resource["Name"] + "Collection"
    namespace = find_latest_namespace(collection_name)
    if namespace is None:
        resource['IsCollectionExist'] = False
    else:
        resource['IsCollectionExist'] = True

def render_resource(resource):
    templateLoader = jinja2.FileSystemLoader(searchpath="/Users/lyang28/workspace/github/rsd-lib-generator/")
    templateEnv = jinja2.Environment(loader=templateLoader)

    template = templateEnv.get_template("resource_template.txt")
    return template.render(resource=resource, need_sushy_utils=NEED_SUSHY_UTILS,
        need_sushy_base=NEED_SUSHY_BASE, need_rsd_lib_utils=NEED_RSD_LIB_UTILS)

def generate_code(module_name):
    namespace = find_latest_namespace(module_name)
    print(namespace)

    resource = get_rsd_resource(namespace, module_name)
    # print('\nAfter expand:\n')
    # print("{0}".format(json.dumps(resource, indent=2, default=set_default)))

    prepare_render_resource(resource)
    # print('\nAfter pre-render:\n')
    # print("{0}".format(json.dumps(resource, indent=2, default=set_default)))

    file_name = './output/' + camelcase_to_underscore_joined(sys.argv[1]) + '.txt'
    f = open(file_name, "w")
    f.write(json.dumps(resource, indent=2, default=set_default))
    f.close()

    result = render_resource(resource)
    print('\nAfter render:\n')
    print(result)

    file_name = './output/' + camelcase_to_underscore_joined(sys.argv[1]) + '.py'
    f = open(file_name, "w")
    f.write(result)
    f.close()

    subprocess.run(["black", "--line-length", "79", file_name])

    return result

def main():
    prepare_schemas()
    # print(SCHEMA_DB.keys())

    generate_code(sys.argv[1])
    # print(code)


if __name__ == '__main__':
    main()
