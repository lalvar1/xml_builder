from module_utils.policy import Policy
from xml.etree.ElementTree import SubElement


class Quota(Policy):
    def __init__(self, name, interval, time_unit, count):
        # super().__init__(name)
        Policy.__init__(self, name)
        self._interval = interval
        self._time_unit = time_unit
        self._count = count
        self._distributed = 'true'

    def to_xml(self):
        xml = self._xml_policy_header('Quota')
        allow = SubElement(xml, 'Allow')
        allow.set("count", str(self._count))

        interval = SubElement(xml, 'Interval')
        interval.text = str(self._interval)

        time_unit = SubElement(xml, 'TimeUnit')
        time_unit.text = str(self._time_unit)

        distributed = SubElement(xml, 'Distributed')
        distributed.text = str(self._distributed)

        return self._xml_document_to_string(xml)
