#!/usr/bin/env python
import os
from zipfile import ZipFile
import re

from module_utils.basic import AnsibleModule
from module_utils.api_proxy_bundle_builder import proxy_builder


def main():
    module = get_playbook_vars()
    api_name = module.params['api_name']
    api_description = module.params['api_description']
    api_base_path = module.params['api_base_path']
    api_team = module.params['api_team']
    api_implementation = module.params['api_implementation']
    api_url = re.match('https?://[^/]*', module.params['api_url'])
    api_url = api_url.group(0)
    api_proxy_base_path = module.params['api_proxy_base_path']
    if api_implementation:
        api_prefix = api_team + '_' + api_implementation
    else:
        api_prefix = api_team
    if not api_base_path.startswith('/', 0, 1):
        api_base_path = '/' + api_base_path
    changed = False
    try:
        proxy_bundle = proxy_builder(api_name, api_team, api_description, api_base_path, api_proxy_base_path)\
            .microgateway_aware(api_prefix, api_url, api_base_path)
        bundle_path = zip_proxy_bundle(api_name, proxy_bundle)
        changed = True
        module.exit_json(changed=changed, msg="Proxy XML bundle was generated successfully", response=bundle_path)
    except Exception as e:
        print(e)
        module.fail_json(changed=changed, msg="Proxy could not be generated, error was:{}".format(e))


def get_playbook_vars():
    module = AnsibleModule(
        argument_spec=dict(
            api_name=dict(required=True, type='str'),
            api_description=dict(required=False, type='str'),
            api_team=dict(required=True, type='str'),
            api_implementation=dict(required=False, type='str'),
            api_base_path=dict(required=True, type='str'),
            api_url=dict(required=True, type='str'),
            api_proxy_base_path=dict(required=True, type='str')
        ),
        supports_check_mode=False,
    )
    return module


def create_folders(api_name):
    if not os.path.isdir('./{}'.format(api_name)):
        os.mkdir('./{}'.format(api_name))
    if not os.path.isdir('./{}/apiproxy'.format(api_name)):
        os.mkdir('./{}/apiproxy'.format(api_name))
    for file in ['manifests', 'proxies', 'targets']:
        if not os.path.isdir('./{}/apiproxy/{}'.format(api_name, file)):
            os.mkdir('./{}/apiproxy/{}'.format(api_name, file))
    os.chdir('./{}/apiproxy'.format(api_name))
    return os.getcwd()


def create_file(content, name, extension, path):
    with open("{}/{}.{}".format(path, name, extension), "w") as f:
        f.write(content)


def create_xml_bundle(api_name, proxy_bundle_instance):
    folders_path = create_folders(api_name)
    proxies_xml = proxy_bundle_instance.proxies_default_xml()
    create_file(proxies_xml, 'default', 'xml', folders_path + '/proxies')
    targets_xml = proxy_bundle_instance.targets_default_xml()
    create_file(targets_xml, 'default', 'xml', folders_path + '/targets')
    main_xml = proxy_bundle_instance.main_xml()
    create_file(main_xml, proxy_bundle_instance.api_name(), 'xml', folders_path)
    manifest_xml = proxy_bundle_instance.manifests_manifest_xml()
    create_file(manifest_xml, 'manifest', 'xml', folders_path + '/manifests')
    for policy in proxy_bundle_instance.policies:
        create_file(policy.to_xml(), policy.name(), 'xml', folders_path + '/policies')
    return folders_path


def zip_proxy_bundle(api_name, proxy_bundle_instance):
    create_xml_bundle(api_name, proxy_bundle_instance)
    os.chdir("../")
    file_paths = []
    zip_name = '{}.zip'.format(api_name)
    for root, directories, files in os.walk("./apiproxy"):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_paths.append(file_path)
    with ZipFile(zip_name, 'w') as zip:
        for file in file_paths:
            zip.write(file)
    bundle_path = os.getcwd() + '/' + zip_name
    return bundle_path


def create_policies(proxy_bundle, api_quota, api_spike_arrest, api_concurrent_rate_limit,
                    none_auth_api_methods):
    if all(api_quota.values()):
        proxy_bundle.add_quota(api_quota['interval'], api_quota['time_unit'], api_quota['count'])
    if all(api_spike_arrest.values()):
        proxy_bundle.add_spike_arrest(api_spike_arrest['value'], api_spike_arrest['unit'])
    if none_auth_api_methods:
        proxy_bundle.skip_authorization(none_auth_api_methods)
    return proxy_bundle


if __name__ == "__main__":
    main()
