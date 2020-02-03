"""
 gnmi_tools - Basic GNMI operations on a device
 gnmi_tools.cmd
 This module implements the command-line parser
"""
import sys
sys.path.append('../gnmi_api/protos')
sys.path.append('../gnmi_api')

import logging
import logging.config
import logging.handlers
import argparse
import json
import os
from pathlib import Path
from .__version__ import __version__ as version
from .__version__ import __doc__ as title
from .utils import EnvVar, TaskOptions
from .api_update import GNMIManagerV2
from gnmi_tools.tasks import *


CERTIFICATE_DIR = Path.home() / '.gnmi_certificates'
GNMI_PORT = 57400

# Default logging configuration - JSON formatted
LOGGING_CONFIG = '''
{
    "version": 1,
    "formatters": {
        "simple": {
            "format": "%(levelname)s: %(message)s"
        },
        "detailed": {
            "format": "%(asctime)s: %(name)s: %(levelname)s: %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "WARN",
            "formatter": "simple"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/gnmi_hello.log",
            "backupCount": 3,
            "maxBytes": 204800,
            "level": "DEBUG",
            "formatter": "detailed"
        }
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "DEBUG"
    },
    "loggers": {
        "ydk": {
            "level": "INFO"
        }
    }
}
'''


def main():
    # Top-level cli parser
    cli_parser = argparse.ArgumentParser(description=title)
    cli_parser.add_argument('-a', '--address', metavar='<address>', action=EnvVar, envvar='DEVICE_IP',
                            help='device IP address, can also be provided via DEVICE_IP environment variable')
    cli_parser.add_argument('-u', '--user', metavar='<user>', action=EnvVar, envvar='GNMI_USER',
                            help='username, can also be provided via GNMI_USER environment variable')
    cli_parser.add_argument('-p', '--password', metavar='<password>', action=EnvVar, envvar='GNMI_PASSWORD',
                            help='password, can also be provided via GNMI_PASSWORD environment variable')
    cli_parser.add_argument('--port', metavar='<port>', type=int, default=GNMI_PORT,
                            help='GNMI TCP port number (default is {port})'.format(port=GNMI_PORT))
    cli_parser.add_argument('--verbose', action='store_true',
                            help='increase output verbosity')
    cli_parser.add_argument('--version', action='version',
                            version='GNMI Hello Version {version}.'.format(version=version))
    cli_parser.add_argument('task', metavar='<task>', type=TaskOptions.task,
                            help='task to be performed ({options})'.format(options=TaskOptions.options()))
    cli_args = cli_parser.parse_args()

    # Logging setup
    logging_config = json.loads(LOGGING_CONFIG)
    console_handler = logging_config.get('handlers', {}).get('console')
    if cli_args.verbose and console_handler is not None:
        console_handler['level'] = 'INFO'

    file_handler = logging_config.get('handlers', {}).get('file')
    if file_handler is not None:
        Path(file_handler['filename']).parent.mkdir(parents=True, exist_ok=True)

    logging.config.dictConfig(logging_config)

    # Delete proxy environment variables to ensure GNMI session does not use proxy
    if os.environ.get('https_proxy'):
        del os.environ['https_proxy']
    if os.environ.get('http_proxy'):
        del os.environ['http_proxy']

    logger = logging.getLogger(__name__)

    device_cert_search = [
        CERTIFICATE_DIR / cli_args.address / 'ems.pem',
        CERTIFICATE_DIR / 'ems.pem',
        Path('ems.pem')
    ]
    for device_cert in device_cert_search:
        if device_cert.exists():
            break
    else:
        device_cert = None

    logger.info('Target: %s, %s', cli_args.address, 'TLS' if device_cert is not None else 'NO_TLS')

    api = GNMIManagerV2(cli_args.address,
                        cli_args.user,
                        cli_args.password,
                        str(GNMI_PORT),
                        str(device_cert) if device_cert is not None else '')

    api.connect()
    if api.is_connected:
        # Dispatch task to the appropriate handler
        result = cli_args.task(api)
        print(result)






