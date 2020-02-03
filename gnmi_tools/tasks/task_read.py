"""
 gnmi_tools - Basic GNMI operations on a device
 gnmi_tasks.tasks.task_read
 Performs a banner read operation

 Banner model:
    module: Cisco-IOS-XR-infra-infra-cfg
      +--rw banners
         +--rw banner* [banner-name]
            +--rw banner-name    Banner
            +--rw banner-text    string
"""
from gnmi_tools.utils import TaskOptions
from gnmi_tools.api_update import GNMIManagerV2


@TaskOptions.register('read_banner')
def run(api: GNMIManagerV2):
    get_complete, response = api.get_config()
    if get_complete:
        return '\n'.join([str(item) for item in response])

    return 'Not complete'
