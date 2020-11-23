import unittest
from module_utils.api_proxy_bundle import ApiProxyBundle
from module_utils.api_proxy_bundle_builder import proxy_builder
from tests.swagger_mock import swagger


class TestProxyPolicies(unittest.TestCase):
    @staticmethod
    def _new_proxy():
        proxy = proxy_builder('test_api_name', 'apim', 'test description', '/api', '/api') \
            .proxy_for_ctportal(swagger, '1.0.0')

        return proxy

    def test_add_quota(self):
        proxy = self._new_proxy()
        proxy.add_quota(1, 'minute', 100)
        self.assertIsInstance(proxy, ApiProxyBundle)

    def test_add_quota_trial(self):
        proxy = self._new_proxy()
        proxy.add_quota_trial()
        self.assertIsInstance(proxy, ApiProxyBundle)

    def test_add_spike_arrest(self):
        proxy = self._new_proxy()
        proxy.add_spike_arrest(100, 'ps')
        self.assertIsInstance(proxy, ApiProxyBundle)

    def test_add_authentication(self):
        proxy = self._new_proxy()
        proxy.add_authentication()
        self.assertIsInstance(proxy, ApiProxyBundle)

    def test_add_none_auth_methods_comma_separated(self):
        proxy = self._new_proxy()
        proxy.skip_authorization('health,test')
        self.assertIsInstance(proxy, ApiProxyBundle)

    def test_add_none_auth_methods_empty(self):
        proxy = self._new_proxy()
        proxy.skip_authorization('')
        self.assertIsInstance(proxy, ApiProxyBundle)

    def test_add_proxy_health(self):
        proxy = self._new_proxy()
        proxy.add_proxy_health("proxy-health", "1.0.1")
        self.assertIsInstance(proxy, ApiProxyBundle)


if __name__ == '__main__':
    unittest.main()
