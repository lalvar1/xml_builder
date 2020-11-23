from xml.etree.ElementTree import Element, SubElement, tostring


class Policy:
    def __init__(self, name):
        self._name = name
        self._conditions = ''

    def name(self):
        return self._name

    def change_name(self, name):
        self._name = name

    def filename(self):
        return self._name + ".xml"

    def ignore_this_methods(self, methods):
        conditions = []
        for method in methods.split(','):
            if '/' in method:
                term = '!(proxy.pathsuffix := "{}")'.format(method)
            else:
                term = '!(proxy.pathsuffix := "/{}")'.format(method)
            conditions.append(term)
        self._conditions = ' and '.join(conditions)

    def add_condition(self, condition):
        self._conditions = condition

    def condition_tostring(self):
        return self._conditions

    def to_xml(self):
        pass

    def _xml_policy_header(self, node_name):
        header = Element(node_name)
        header.set('async', 'false')
        header.set('continueOnError', 'false')
        header.set('enabled', 'true')
        header.set('name', self.name())

        display_name = SubElement(header, 'DisplayName')
        display_name.text = self.name()

        return header

    def add_step_xml(self, parent_xml_node):
        step = SubElement(parent_xml_node, 'Step')
        name = SubElement(step, 'Name')
        name.text = self.name()
        condition = SubElement(step, 'Condition')
        condition.text = self.condition_tostring()

    def _xml_document_to_string(self, document):
        return tostring(document, encoding='utf8', method='xml').decode()

    def skip_verb_options(self):
        if not self._conditions:
            self._conditions = 'request.verb != "OPTIONS"'
        else:
            if self._conditions != 'request.verb != "OPTIONS"':
                self._conditions = 'request.verb != "OPTIONS" and ' + self._conditions
