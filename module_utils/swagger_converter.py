import json
import re
from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement
swagger_data = "swagger.json"


def _swagger_to_xml(swagger_data):
    swagger_data = read_file(swagger_data)
    if 'openapi' in swagger_data:
        return parse_open_api(swagger_data)

    top = Element('Flows')
    description, flow_name, condition = '', '', ''
    for path, path_info in swagger_data['paths'].items():
        # request = path['parameters']
        # response = path['responses']
        # method = next(iter(path))
        method = list(path_info.keys())[0]
        if 'operationId' in path_info[method]:
            flow_name = path_info[method]['operationId']
        else:
            flow_name = method + ' ' + path
        if 'summary' in path_info[method]:
            description = path_info[method]['summary']
        condition = '(proxy.pathsuffix MatchesPath "{}") and (request.verb = "{}")'.\
            format(re.sub('{.+?}', '*', path), method.upper())
        top = define_xml_tree(top, flow_name, description, condition)

    return top


def define_xml_tree(top, flow_name, description, condition):
    child = SubElement(top, 'Flow')
    child.set('name', flow_name)
    sub_element_child = SubElement(child, 'Description')
    if description:
        sub_element_child.text = description
    SubElement(child, 'Request')
    SubElement(child, 'Response')
    sub_element_child = SubElement(child, 'Condition')
    sub_element_child.text = condition
    return top


def parse_open_api(json_data):
    top = Element('Flows')
    description, flow_name, condition = '', '', ''
    for path, path_info in json_data['paths'].items():
        methods_list = list(path_info.keys())
        for method in methods_list:
            if method.lower() in ['get', 'post', 'put', 'patch', 'delete']:
                if 'tags' in path_info[method]:
                    flow_name = path_info[method]['tags'][0]
                else:
                    flow_name = method + ' ' + path
                # description = path_info[method]['summary']
                condition = '(proxy.pathsuffix MatchesPath "{}") and (request.verb = "{}")'. \
                    format(re.sub('{.+?}', '*', path), method.upper())
                top = define_xml_tree(top, flow_name, description, condition)
        else:
            continue
    return top


def read_file(file):
    try:
        f = open(file, "r")
        data = f.read()
        data = json.loads(data)
    except Exception as e:
        print('This is not a File. Error was {}. Proceed to load json variable and not file'.format(e))
        data = json.loads(file)
    return data


def to_pretty_xml(xml):
    doc = minidom.parseString(xml)
    print(doc.toprettyxml())


# if __name__ == "__main__":
#     flow = _swagger_to_xml(swagger_data)
#     print(flow)
#     xml = tostring(flow, encoding='utf8', method='xml')
#     print(xml)
#     to_pretty_xml(xml)
