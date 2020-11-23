from module_utils.policy import Policy
from xml.etree.ElementTree import SubElement


class RaiseFault(Policy):
    def __init__(self, name):
        # super().__init__(name)
        Policy.__init__(self, name)
        self._status_code = ''
        self._reason_phrase = ''
        self._json_payload = ''

    def fault_response(self, http_code, http_phrase, json_payload):
        self._status_code = http_code
        self._reason_phrase = http_phrase
        self._json_payload = json_payload

    def to_xml(self):
        xml = self._xml_policy_header('RaiseFault')

        ignore_unresolved_variables = SubElement(xml, 'IgnoreUnresolvedVariables')
        ignore_unresolved_variables.text = "false"

        fault_response = SubElement(xml, 'FaultResponse')
        set_node = SubElement(fault_response, 'Set')
        status_code = SubElement(set_node, 'StatusCode')
        status_code.text = str(self._status_code)
        reason_phrase = SubElement(set_node, 'ReasonPhrase')
        reason_phrase.text = self._reason_phrase
        payload = SubElement(set_node, 'Payload')
        payload.set('contentType', 'application/json;')
        payload.text = str(self._json_payload)

        return self._xml_document_to_string(xml)
