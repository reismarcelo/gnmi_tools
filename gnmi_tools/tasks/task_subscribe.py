"""
 gnmi_tools - Basic GNMI operations on a device
 gnmi_tools.tasks.task_subscribe
 Performs subscribe operation operation

 OC model:
    module: Cisco-IOS-XR-infra-infra-cfg
      +--rw banners
         +--rw banner* [banner-name]
            +--rw banner-name    Banner
            +--rw banner-text    string
"""
import logging
import time
from gnmi_tools.utils import TaskOptions
from gnmi_tools.api_update import GNMIManagerV2

# TIME_BUDGET indicates how many seconds the subscriber will be on the subscription loop
TIME_BUDGET = 300


@TaskOptions.register('subscribe')
def run(api: GNMIManagerV2):
    logger = logging.getLogger('subscribe')

    subs = api.subscribe(
        requests=['openconfig-network-instance:network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor'],
        encoding='PROTO',
        sample_rate=5,
        stream_mode='STREAM',
        subscribe_mode='SAMPLE'
    )

    time_budget = TIME_BUDGET
    ts_last = time.time()
    sample_list = []
    for sample in subs:
        ts_new = time.time()
        time_budget -= ts_new - ts_last
        ts_last = ts_new
        if time_budget < 0:
            logger.info('Time budget expired, closing subscription')
            break

        logger.info(sample)
        sample_list.append(sample)

    return '\n'.join(sample_list)

