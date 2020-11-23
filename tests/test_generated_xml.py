import unittest
from module_utils.api_proxy_bundle_builder import proxy_builder
from module_utils.api_proxy_bundle import ApiProxyBundle
from tests.swagger_mock import swagger


class TestProxyPolicies(unittest.TestCase):
    @staticmethod
    def _new_proxy():
        proxy = proxy_builder('test_api_name', 'apim', 'test description', '/api', '/api') \
            .proxy_for_ctportal(swagger, '1.0.0')
        return proxy

    def test_create_proxies_xml(self):
        proxy = self._new_proxy()
        proxy.proxies_default_xml()
        self.assertIsInstance(proxy, ApiProxyBundle)

    def test_create_targets_xml(self):
        proxy = self._new_proxy()
        proxy.targets_default_xml()
        self.assertIsInstance(proxy, ApiProxyBundle)

    def test_create_main_xml(self):
        proxy = self._new_proxy()
        proxy.main_xml()
        self.assertIsInstance(proxy, ApiProxyBundle)

    def test_create_manifest_xml(self):
        proxy = self._new_proxy()
        proxy.manifests_manifest_xml()
        self.assertIsInstance(proxy, ApiProxyBundle)

    # def test_create_default_xml(self):
    #     proxy = ApiProxyBundle('test_api_name', 'test description', swagger, '/api')
    #     proxy.policies()
    #     self.assertIsInstance(proxy, ApiProxyBundle)


if __name__ == '__main__':
    unittest.main()
