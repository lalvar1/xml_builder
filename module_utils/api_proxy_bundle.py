from xml.etree.ElementTree import Element, SubElement, tostring
from module_utils.swagger_converter import _swagger_to_xml
from module_utils.quota import Quota
from module_utils.spike_arrest import SpikeArrest
from module_utils.key_value_map_operations import KeyValueMapOperations
from module_utils.authentication import Authentication
from module_utils.fault_rule import FaultRule
from module_utils.assign_message import AssignMessage
from module_utils.raise_fault import RaiseFault
from module_utils.cors import Cors


class ApiProxyBundle:
    def __init__(self, proxy_name, team_name, description, base_path, api_proxy_base_path):
        self._authentication_policy = Authentication()
        self._swagger_xml = ''
        self._description = description
        self.policies = []
        self._pre_flow_policies = []
        self._pre_flow_response_policies = []
        self._target_endpoint_policies = []
        self._fault_rules = []
        self._base_path = base_path
        self._api_proxy_base_path = api_proxy_base_path
        self._api_name = proxy_name
        self._api_team = team_name
        self._name = self.set_saas_prefix("SaaS")
        self._target_connection_element = self._define_saas_target_element()

    def __str__(self):
        return "Proxy Bundle Generator Class"

    def api_name(self):
        return self._name

    def import_swagger(self, swagger_json):
        self._swagger_xml = _swagger_to_xml(swagger_json)

    def skip_authorization(self, methods):
        self._authentication_policy.ignore_this_methods(methods)

    @staticmethod
    def _xml_document_to_string(document):
        return tostring(document, encoding='utf8', method='xml').decode()

    def add_authentication(self):
        environment_values = KeyValueMapOperations(self._name)
        self.policies.append(environment_values)
        self._add_policy_pre_flow(environment_values)
        authentication = Authentication()
        self._authentication_policy = authentication
        self._add_policy_pre_flow(authentication)

    def add_quota_trial(self):
        quota = Quota('QuotaTrial', 1, 'month', 10000)
        self._add_policy_pre_flow(quota)
        fault_rule = self._new_fault_rule('RiseMessageTrialQuotaExceeded', 'ratelimit.QuotaTrial.failed = true')

        message = AssignMessage('TrialQuotaExceeded')
        message.return_json({
            "error": "429",
            "description": "Quota Exceeded, please contact the Api Management Team"
        })
        message.add_condition('fault.name Matches "QuotaViolation"')
        self.policies.append(message)
        fault_rule.add_policy(message)

    def add_quota(self, interval, time_unit, count):
        quota = Quota('Quota', interval, time_unit, count)
        self._add_policy_pre_flow(quota)

    def _new_fault_rule(self, name, condition):
        fault_rule = FaultRule(name, condition)
        self._fault_rules.append(fault_rule)
        return fault_rule

    def add_spike_arrest(self, spike_arrest_value, unit):
        spike_arrest = SpikeArrest(spike_arrest_value, unit)
        self._add_policy_pre_flow(spike_arrest)

    def add_cors(self, allow_origin, allow_headers):
        for policy in self.policies:
            policy.skip_verb_options()

        cors_policy = Cors(allow_origin, allow_headers)

        flow = SubElement(self._swagger_xml, 'Flow')
        flow.set("name", "CORS preflight")
        cors_policy.add_cors_step_xml(flow)

        self._add_policy_pre_flow_response(cors_policy)

        fault_rule = self._new_fault_rule('cors-fault-rule', '(response.status.code != "200")')
        fault_rule.add_policy(cors_policy)

    def _add_policy_pre_flow_response(self, policy):
        self.policies.append(policy)
        self._pre_flow_response_policies.append(policy)

    def _add_policy_pre_flow(self, policy):
        self.policies.append(policy)
        self._pre_flow_policies.append(policy)

    def _add_target_endpoint_policy(self, policy):
        self.policies.append(policy)
        self._target_endpoint_policies.append(policy)

    def add_proxy_health(self, web_method_name, api_proxy_tag):
        fault_policy = RaiseFault("ProxyHealth")
        fault_policy.fault_response(
            200,
            "Proxy OK!",
            {"proxy-status": "running", "environment": "{environment.name}", "Proxy Version": api_proxy_tag})
        fault_policy.add_condition('proxy.pathsuffix MatchesPath "/{}"'.format(web_method_name))
        self._add_policy_pre_flow(fault_policy)

    def targets_default_xml(self):
        target_endpoint = Element('TargetEndpoint')
        target_endpoint.set('name', 'default')

        SubElement(target_endpoint, 'Description')
        target_fault_rules = SubElement(target_endpoint, 'FaultRules')
        for p in self._pre_flow_response_policies:
            if p._name == "add-cors":
                fault_rule = self._new_fault_rule('cors-fault-rule', '(response.status.code != "200")')
                fault_rule.add_policy(p)
                fault_rule.add_to_parent_node(target_fault_rules)

        pre_flow = SubElement(target_endpoint, 'PreFlow')
        pre_flow.set('name', 'PreFlow')
        pre_flow_request = SubElement(pre_flow, 'Request')
        for p in self._target_endpoint_policies:
            p.add_step_xml(pre_flow_request)
        SubElement(pre_flow, 'Response')

        SubElement(target_endpoint, 'Flows')

        post_flow = SubElement(target_endpoint, 'PostFlow')
        post_flow.set('name', 'PostFlow')
        post_flow_request = SubElement(post_flow, 'Request')
        for p in self._target_endpoint_policies:
            p.add_step_xml(post_flow_request)
        SubElement(post_flow, 'Response')

        target_endpoint.append(self._target_connection_element)

        for p in self._target_endpoint_policies:
            default_rule = SubElement(target_endpoint, 'DefaultFaultRule')
            default_rule.set('name', 'default_rule')
            always_enforce = SubElement(default_rule, 'AlwaysEnforce')
            always_enforce.text = 'true'
            p.add_step_xml(default_rule)

        return self._xml_document_to_string(target_endpoint)

    def _define_saas_target_element(self):
        http_target_connection = Element('HTTPTargetConnection')
        server_element = SubElement(http_target_connection, 'LoadBalancer')
        server = SubElement(server_element, 'Server')
        server.set('name', self._name)
        path = SubElement(http_target_connection, 'Path')
        path.text = self._base_path
        return http_target_connection

    def define_url_in_target(self, api_url, api_base_path):
        http_target_connection = Element('HTTPTargetConnection')
        url = SubElement(http_target_connection, 'URL')
        url.text = api_url + api_base_path
        self._target_connection_element = http_target_connection

    def manifests_manifest_xml(self):
        manifest = Element('Manifest')
        manifest.set('name', 'manifest')

        policies = SubElement(manifest, 'Policies')
        for policy in self.policies:
            policy_xml_node = SubElement(policies, 'VersionInfo')
            policy_xml_node.set('resourceName', policy.name())

        proxy_endpoints = SubElement(manifest, 'ProxyEndpoints')
        version_info = SubElement(proxy_endpoints, 'VersionInfo')
        version_info.set('resourceName', 'default')

        target_endpoints = SubElement(manifest, 'TargetEndpoints')
        version_info = SubElement(target_endpoints, 'VersionInfo')
        version_info.set('resourceName', 'default')

        return self._xml_document_to_string(manifest)

    def proxies_default_xml(self):
        proxy_endpoint = Element('ProxyEndpoint')
        proxy_endpoint.set('name', 'default')

        SubElement(proxy_endpoint, 'Description')

        pre_flow = SubElement(proxy_endpoint, 'PreFlow')
        pre_flow.set('name', 'PreFlow')
        request = SubElement(pre_flow, 'Request')

        for p in self._pre_flow_policies:
            p.add_step_xml(request)

        response = SubElement(pre_flow, 'Response')
        for p in self._pre_flow_response_policies:
            p.add_step_xml(response)

        post_flow = SubElement(proxy_endpoint, 'PostFlow')
        SubElement(post_flow, 'Request')
        SubElement(post_flow, 'Response')

        fault_rules_xml = SubElement(proxy_endpoint, 'FaultRules')
        for f in self._fault_rules:
            f.add_to_parent_node(fault_rules_xml)

        if self._swagger_xml:
            proxy_endpoint.append(self._swagger_xml)
        else:
            SubElement(proxy_endpoint, 'Flows')

        http_proxy_connection = SubElement(proxy_endpoint, 'HTTPProxyConnection')
        base_path = SubElement(http_proxy_connection, 'BasePath')
        base_path.text = '/{}/{}{}'.format(self._api_team, self._api_name, self._api_proxy_base_path)
        SubElement(http_proxy_connection, 'Properties')
        virtual_host = SubElement(http_proxy_connection, 'VirtualHost')
        virtual_host.text = 'ey'

        for p in self._pre_flow_response_policies:
            if p._name == "add-cors":
                route_rule = SubElement(proxy_endpoint, 'RouteRule')
                route_rule.set('name', 'NoRoute')
                target_endpoint = SubElement(route_rule, 'Condition')
                target_endpoint.text = 'request.verb == "OPTIONS" AND '\
                    'request.header.origin != null AND ' \
                    'request.header.Access-Control-Request-Method != null'

        route_rule = SubElement(proxy_endpoint, 'RouteRule')
        route_rule.set('name', 'default')
        target_endpoint = SubElement(route_rule, 'TargetEndpoint')
        target_endpoint.text = 'default'

        return self._xml_document_to_string(proxy_endpoint)

    def main_xml_filename(self):
        return self._name + ".xml"

    def main_xml(self):
        api_proxy = Element('APIProxy')
        api_proxy.set('name', self._name)

        base_paths = SubElement(api_proxy, 'BasePaths')
        base_paths.text = '/{}/{}{}'.format(self._api_team, self._api_name, self._api_proxy_base_path)

        configuration_version = SubElement(api_proxy, 'ConfigurationVersion')
        configuration_version.set('majorVersion', '4')
        configuration_version.set('minorVersion', '0')

        description = SubElement(api_proxy, 'Description')
        description.text = self._description

        display_name = SubElement(api_proxy, 'DisplayName')
        display_name.text = self._name

        policies = SubElement(api_proxy, 'Policies')
        for policy in self.policies:
            policy_xml_node = SubElement(policies, 'Policy')
            policy_xml_node.text = policy.name()

        proxy_endpoints = SubElement(api_proxy, 'ProxyEndpoints')
        proxy_endpoint = SubElement(proxy_endpoints, 'ProxyEndpoint')
        proxy_endpoint.text = "default"

        resources = SubElement(api_proxy, 'Resources')
        resource = SubElement(resources, 'Resource')
        resource.text = "openapi://association.json"

        target_endpoints = SubElement(api_proxy, 'TargetEndpoints')
        target_endpoint = SubElement(target_endpoints, 'TargetEndpoint')
        target_endpoint.text = "default"

        return self._xml_document_to_string(api_proxy)

    def set_microgateway_prefix(self, prefix):
        self._name = prefix + "_" + self._name

    def set_saas_prefix(self, prefix):
        return prefix + "_" + self._api_team + "_" + self._api_name
