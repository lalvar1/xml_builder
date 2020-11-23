from module_utils.api_proxy_bundle import ApiProxyBundle


def proxy_builder(proxy_name, api_team, description, base_path, api_proxy_base_path):
    return ApiProxyBundleBuilder(proxy_name, api_team, description, base_path, api_proxy_base_path)


class ApiProxyBundleBuilder:

    def __init__(self, proxy_name, api_team, description, base_path, api_proxy_base_path):
        self._proxy_bundle = ApiProxyBundle(proxy_name, api_team, description, base_path, api_proxy_base_path)

    def proxy_for_ctportal(self, swagger_json, api_proxy_tag):
        self._proxy_bundle.add_quota_trial()
        self._proxy_bundle.add_proxy_health("proxy-health", api_proxy_tag)
        self._proxy_bundle.add_authentication()
        self._proxy_bundle.import_swagger(swagger_json)
        return self._proxy_bundle

    def microgateway_aware(self, prefix, api_url, api_base_path):
        self._proxy_bundle.set_microgateway_prefix("edgemicro_" + prefix)
        self._proxy_bundle.define_url_in_target(api_url, api_base_path)
        return self._proxy_bundle
