from module_utils.policy import Policy
from xml.etree.ElementTree import SubElement


class KeyValueMapOperations(Policy):
    def __init__(self, map_id):
        Policy.__init__(self, 'MapEnvironmentValues')
        # super().__init__('MapEnvironmentValues')
        self._map_Id = map_id

    def to_xml(self):
        kvm = self._xml_policy_header('KeyValueMapOperations')
        kvm.set('mapIdentifier', self._map_Id)
        expiry_time = SubElement(kvm, 'ExpiryTimeInSecs')
        expiry_time.text = '3600'  # equals to one hour

        scope = SubElement(kvm, 'Scope')
        scope.text = 'environment'

        self.__get_xml_node(kvm, 'context.issuerURL', 'IssuerURL')
        self.__get_xml_node(kvm, 'context.tenant', 'Tenant')
        self.__get_xml_node(kvm, 'context.applicationId', 'ApplicationId')

        return self._xml_document_to_string(kvm)

    @staticmethod
    def __get_xml_node(parent_node, pipeline_var, kvm_key):
        get = SubElement(parent_node, 'Get')
        get.set('assignTo', pipeline_var)
        key = SubElement(get, 'Key')
        parameter = SubElement(key, 'Parameter')
        parameter.text = kvm_key

        return get
