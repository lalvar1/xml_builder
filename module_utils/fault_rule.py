from xml.etree.ElementTree import SubElement


class FaultRule:
    def __init__(self, name, condition):
        self._name = name
        self._condition = condition
        self._policies = []

    def add_policy(self, policy):
        self._policies.append(policy)

    def add_to_parent_node(self, parent_xml_node):
        fault_rule = SubElement(parent_xml_node, 'FaultRule')
        fault_rule.set("name", self._name)
        condition = SubElement(fault_rule, 'Condition')
        condition.text = self._condition

        for p in self._policies:
            p.add_step_xml(fault_rule)
