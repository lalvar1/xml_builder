import unittest
from module_utils.api_proxy_bundle import ApiProxyBundle


class TestProxyInstance(unittest.TestCase):
    def test_class_instance(self):
        proxy = ApiProxyBundle('test_api_name', 'apim', 'test description', '/api', '/api')
        self.assertIsInstance(proxy, ApiProxyBundle)

    def test_none_swagger(self):
        proxy = ApiProxyBundle('test_api_name', 'apim', 'test description', '/api', '/api')
        self.assertIsInstance(proxy, ApiProxyBundle)

    def test_none_api_name(self):
        proxy = ApiProxyBundle('', 'apim', 'test description', '/api', '/api')
        self.assertIsInstance(proxy, ApiProxyBundle)

    def test_none_description(self):
        proxy = ApiProxyBundle('test_api_name', 'apim', '', '/api', '/api')
        self.assertIsInstance(proxy, ApiProxyBundle)

    def test_none_base_path(self):
        proxy = ApiProxyBundle('test_api_name', 'apim', 'test description', '', '')
        self.assertIsInstance(proxy, ApiProxyBundle)

    def test_none_data(self):
        proxy = ApiProxyBundle('', '', '', '', '')
        self.assertIsInstance(proxy, ApiProxyBundle)


if __name__ == '__main__':
    unittest.main()
