from module_utils.policy import Policy
from xml.etree.ElementTree import SubElement


class AssignMessage(Policy):
    def __init__(self, name):
        # super().__init__(name)
        Policy.__init__(self, name)
        self._json_payload = ""

    def return_json(self, json):
        self._json_payload = str(json)

    def to_xml(self):
        xml = self._xml_policy_header('AssignMessage')
        ignore_unresolved_vars = SubElement(xml, 'IgnoreUnresolvedVariables')
        ignore_unresolved_vars.text = "false"
        assign_to = SubElement(xml, 'AssignTo')
        assign_to.set("createNew", "false")
        assign_to.set("transport", "http")
        assign_to.set("type", "response")

        set = SubElement(xml, 'Set')
        payload = SubElement(set, 'Payload')
        payload.set("contentType", "application/json;")
        payload.text = self._json_payload

        return self._xml_document_to_string(xml)
