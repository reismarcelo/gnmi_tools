#! /usr/bin/env python3
"""
gnmi_tools - Basic GNMI operations on a device

"""
import re
import sys
sys.path.append('gnmi_api/protos')
sys.path.append('gnmi_api')

from gnmi_tools.cmd import main

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(main())
