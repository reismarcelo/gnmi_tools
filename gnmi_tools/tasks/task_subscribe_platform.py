"""
 gnmi_tools - Basic GNMI operations on a device
 gnmi_tools.tasks.task_subscribe_platform
 Performs subscribe operation operation

 Subscriptions model:
    module: openconfig-platform
      +--rw components
         +--rw component* [name]
            +--rw name                  -> ../config/name
            +--rw config
            |  +--rw name?   string
            +--ro state
            |  +--ro name?               string
            |  +--ro type?               union
            |  +--ro id?                 string
            |  +--ro location?           string
            |  +--ro description?        string
            |  +--ro mfg-name?           string
            |  +--ro mfg-date?           oc-yang:date
            |  +--ro hardware-version?   string
            |  +--ro firmware-version?   string
            |  +--ro software-version?   string
            |  +--ro serial-no?          string
            |  +--ro part-no?            string
            |  +--ro removable?          boolean
            |  +--ro oper-status?        identityref
            |  +--ro empty?              boolean
            |  +--ro parent?             -> ../../config/name
            |  +--ro temperature
            |  |  +--ro instant?           decimal64
            |  |  +--ro avg?               decimal64
            |  |  +--ro min?               decimal64
            |  |  +--ro max?               decimal64
            |  |  +--ro interval?          oc-types:stat-interval
            |  |  +--ro min-time?          oc-types:timeticks64
            |  |  +--ro max-time?          oc-types:timeticks64
            |  |  +--ro alarm-status?      boolean
            |  |  +--ro alarm-threshold?   uint32
            |  |  +--ro alarm-severity?    identityref
            |  +--ro memory
            |  |  +--ro available?   uint64
            |  |  +--ro utilized?    uint64
            |  +--ro allocated-power?    uint32
            |  +--ro used-power?         uint32
            +--rw properties
            |  +--rw property* [name]
            |     +--rw name      -> ../config/name
            |     +--rw config
            |     |  +--rw name?    string
            |     |  +--rw value?   union
            |     +--ro state
            |        +--ro name?           string
            |        +--ro value?          union
            |        +--ro configurable?   boolean
            +--rw subcomponents
            |  +--rw subcomponent* [name]
            |     +--rw name      -> ../config/name
            |     +--rw config
            |     |  +--rw name?   -> ../../../../../component/config/name
            |     +--ro state
            |        +--ro name?   -> ../../../../../component/config/name
            +--rw chassis
            |  +--rw config
            |  +--ro state
            +--rw port
            |  +--rw config
            |  +--ro state
            +--rw power-supply
            |  +--rw config
            |  +--ro state
            +--rw fan
            |  +--rw config
            |  +--ro state
            +--rw fabric
            |  +--rw config
            |  +--ro state
            +--rw storage
            |  +--rw config
            |  +--ro state
            +--rw cpu
            |  +--rw config
            |  +--ro state
            +--rw integrated-circuit
            |  +--rw config
            |  +--ro state
            +--rw backplane
               +--rw config
               +--ro state

"""
import logging
import time
from gnmi_tools.utils import TaskOptions
from gnmi_tools.api_update import GNMIManagerV2

# TIME_BUDGET indicates how many seconds the subscriber will be on the subscription loop
TIME_BUDGET = 120


@TaskOptions.register('subscribe-platform')
def run(api: GNMIManagerV2):
    logger = logging.getLogger('subscribe-platform')

    subs = api.subscribe(
        requests=[
            'openconfig-platform:components/component',
        ],
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

    return 'Subscription samples saved to log.'

