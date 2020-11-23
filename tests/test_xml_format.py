import unittest
from xmlunittest import XmlTestMixin
from module_utils.api_proxy_bundle_builder import proxy_builder
from tests.swagger_mock import swagger


class CustomTestCase(unittest.TestCase, XmlTestMixin):
    @staticmethod
    def _new_proxy():
        proxy = proxy_builder('test_api_name', 'apim', 'test description', '/api', '/api').\
                proxy_for_ctportal(swagger, '1.0.0')
        return proxy

    @staticmethod
    def _new_microgateway():
        micro_proxy = proxy_builder('test_api_name', 'apim', 'test description', '/api', '/api').\
                      microgateway_aware('my-api-team', 'www.google.com', '/api')
        return micro_proxy

    def test_quota_trial(self):
        proxy = self._new_proxy()
        proxy.add_quota_trial()
        data = proxy.policies[0].to_xml()
        self.assertXmlDocument(data.encode())
        # root = self.assertXmlDocument(data.encode())
        # self.assertXmlNamespace(root, 'ns', 'uri')

    def test_quota(self):
        proxy = self._new_proxy()
        proxy.add_quota(1, 'minute', 100)
        data = proxy.policies[0].to_xml()
        self.assertXmlDocument(data.encode())

    # def test_concurrent_limit_rate(self):
    #     proxy = self._new_proxy()
    #     proxy.add_concurrent_rate_limit(100, 10)
    #     data = proxy.policies[0].to_xml()
    #     self.assertXmlDocument(data.encode())

    def test_spike_arrest(self):
        proxy = self._new_proxy()
        proxy.add_spike_arrest(100, 'ps')
        data = proxy.policies[0].to_xml()
        self.assertXmlDocument(data.encode())

    def test_authentication(self):
        proxy = self._new_proxy()
        proxy.add_authentication()
        data = proxy.policies[0].to_xml()
        self.assertXmlDocument(data.encode())

    def test_proxy_health(self):
        proxy = self._new_proxy()
        proxy.add_proxy_health("proxy-health", "1.0.1")
        data = proxy.policies[0].to_xml()
        self.assertXmlDocument(data.encode())

    def test_proxies_xml(self):
        proxy = self._new_proxy()
        data = proxy.proxies_default_xml()
        self.assertXmlDocument(data.encode())

    def test_targets_xml(self):
        proxy = self._new_proxy()
        data = proxy.targets_default_xml()
        self.assertXmlDocument(data.encode())

    def test_main_xml(self):
        proxy = self._new_proxy()
        data = proxy.main_xml()
        self.assertXmlDocument(data.encode())

    def test_manifest_xml(self):
        proxy = self._new_proxy()
        data = proxy.manifests_manifest_xml()
        self.assertXmlDocument(data.encode())

    def test_microgateway_proxies_xml(self):
        proxy = self._new_microgateway()
        data = proxy.proxies_default_xml()
        self.assertXmlDocument(data.encode())

    def test_microgateway_targets_xml(self):
        proxy = self._new_microgateway()
        data = proxy.targets_default_xml()
        self.assertXmlDocument(data.encode())

    def test_microgateway_main_xml(self):
        proxy = self._new_microgateway()
        data = proxy.main_xml()
        self.assertXmlDocument(data.encode())

    def test_microgateway_manifest_xml(self):
        proxy = self._new_microgateway()
        data = proxy.manifests_manifest_xml()
        self.assertXmlDocument(data.encode())


if __name__ == '__main__':
    unittest.main()
