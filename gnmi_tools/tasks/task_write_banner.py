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
from gnmi_api.protos.gnmi_pb2 import UpdateResult


@TaskOptions.register('write_banner')
def run(api: GNMIManagerV2):
    json_request = '''
    {
        "Cisco-IOS-XR-infra-infra-cfg:banners": {
            "banner": [
                {
                    "banner-name": "motd", 
                    "banner-text": "# Yet Another Banner #"
                }
            ]
        }
    }
    '''
    set_complete, set_response = api.set(ParsedSetRequest(json.loads(json_request)).update_request)
    if not set_complete:
        return 'Error on set'

    return '\n'.join([f'{response.path}: {UpdateResult.Operation.Name(response.op)}' for response in set_response.response])

