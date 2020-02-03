"""
 gnmi_tools - Basic GNMI operations on a device
 gnmi_tools.tasks.task_write
 Performs a banner write operation

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
from gnmi_api.responses import ParsedSetRequest


@TaskOptions.register('write_banner')
def run(api: GNMIManagerV2):
    json_request = '''
        update {
            path {
                elem {
                    name: "Cisco-IOS-XR-infra-infra-cfg:banners"
                }
            }
            val {
                json_ietf_val: "{"banner": [{"banner-name": "motd", "banner-text": "c This is a test json banner c"}]}"
            }
        }
    '''
    set_request = ParsedSetRequest(json.loads(json_request))
    set_complete, response_list = api.set(set_request.update_request)
    if not set_complete:
        return 'Error on set'

    return '\n'.join([json.dumps(response.json, indent=2) for response in response_list])

