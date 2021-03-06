"""
 gnmi_tools - Basic GNMI operations on a device
 gnmi_tools.tasks.task_read_all
 Read all config on device

 Banner model:
    module: Cisco-IOS-XR-infra-infra-cfg
      +--rw banners
         +--rw banner* [banner-name]
            +--rw banner-name    Banner
            +--rw banner-text    string
"""
import json
from gnmi_tools.utils import TaskOptions
from gnmi_tools.api_update import GNMIManagerV2


@TaskOptions.register('read_all')
def run(api: GNMIManagerV2):
    get_complete, response_list = api.get_config(encoding='JSON_IETF')
    if not get_complete:
        return 'Error on get_config'

    return '\n'.join([json.dumps(response.json, indent=2) for response in response_list])
