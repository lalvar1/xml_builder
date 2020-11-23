from module_utils.policy import Policy
from xml.etree.ElementTree import SubElement


class SpikeArrest(Policy):
    def __init__(self, spike_arrest_value, unit):
        # super().__init__('SpikeArrest')
        Policy.__init__(self, 'SpikeArrest')
        self.spike_arrest_value = spike_arrest_value
        self.unit = unit

    def to_xml(self):
        spike_arrest = self._xml_policy_header('SpikeArrest')

        rate = SubElement(spike_arrest, 'Rate')
        value = str(self.spike_arrest_value) + self.unit
        rate.text = value

        use_effective_count = SubElement(spike_arrest, 'UseEffectiveCount')
        use_effective_count.text = 'true'

        return self._xml_document_to_string(spike_arrest)
