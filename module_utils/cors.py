from module_utils.policy import Policy
from xml.etree.ElementTree import SubElement


class Cors(Policy):
    def __init__(self, allow_origin, allow_headers):
        Policy.__init__(self, "add-cors")
        self.allow_origin = allow_origin
        self.allow_headers = allow_headers

    def to_xml(self):
        xml = self._xml_policy_header('AssignMessage')
        set_node = SubElement(xml, 'Set')
        set_headers = SubElement(set_node, 'Headers')

        # use one url or *
        self.add_header(set_headers, "Access-Control-Allow-Origin", self.allow_origin)
        # use comma separated values or *. Eg.:origin, Authorization, accept, content-type
        self.add_header(set_headers, "Access-Control-Allow-Headers", self.allow_headers)
        self.add_header(set_headers, "Access-Control-Max-Age", "3628800")
        self.add_header(set_headers, "Access-Control-Allow-Methods", "GET, PUT, PATCH, POST, DELETE, OPTIONS")
        self.add_header(set_headers, "Access-Control-Allow-Credentials", "true")

        ignore_unresolved_vars = SubElement(xml, 'IgnoreUnresolvedVariables')
        ignore_unresolved_vars.text = "true"

        assign_to = SubElement(xml, 'AssignTo')
        assign_to.set("createNew", "false")
        assign_to.set("transport", "http")
        assign_to.set("type", "response")

        return self._xml_document_to_string(xml)

    def add_cors_step_xml(self, parent_xml_node):
        description = SubElement(parent_xml_node, 'Description')
        description.text = self.name()
        SubElement(parent_xml_node, 'Request')
        response = SubElement(parent_xml_node, 'Response')
        step = SubElement(response, 'Step')
        name = SubElement(step, 'Name')
        name.text = self.name()
        condition = SubElement(parent_xml_node, 'Condition')
        condition.text = "request.verb = 'OPTIONS'"

    @staticmethod
    def add_header(set_headers, name_attr, inner_text):
        header = SubElement(set_headers, 'Header')
        header.set("name", name_attr)
        header.text = inner_text
