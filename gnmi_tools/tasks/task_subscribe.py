"""
 gnmi_tools - Basic GNMI operations on a device
 gnmi_tools.tasks.task_subscribe
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


@TaskOptions.register('subscribe')
def run(api: GNMIManagerV2):
    subs = api.subscribe(
        requests=['openconfig-network-instance:network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor'],
        encoding='PROTO',
        sample_rate=5,
        stream_mode='STREAM',
        subscribe_mode='SAMPLE'
    )
    for sample in subs:
        print(sample)

    return 'Completed'

