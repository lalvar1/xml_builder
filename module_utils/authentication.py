from module_utils.policy import Policy
from xml.etree.ElementTree import SubElement


class Authentication(Policy):
    def __init__(self):
        Policy.__init__(self, 'Authentication')
        # super(Authentication, self).__init__('Authentication')

    def to_xml(self):
        flow_callout = self._xml_policy_header('FlowCallout')

        shared_flow_bundle = SubElement(flow_callout, 'SharedFlowBundle')
        shared_flow_bundle.text = 'Microsoft-SSO-Token-Validation'

        SubElement(flow_callout, 'FaultRules')
        SubElement(flow_callout, 'Properties')

        return self._xml_document_to_string(flow_callout)
