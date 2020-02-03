"""
 gnmi_tools - Basic GNMI operations on a device
 gnmi_tasks.tasks.task_write
 Performs a banner write operation

 Banner model:
    module: Cisco-IOS-XR-infra-infra-cfg
      +--rw banners
         +--rw banner* [banner-name]
            +--rw banner-name    Banner
            +--rw banner-text    string
"""
from gnmi_tools.utils import TaskOptions


@TaskOptions.register('write_banner')
def run(provider):
    crud = CRUDService()

    banners = xr_infra_cfg.Banners()
    banner_entry = xr_infra_cfg.Banners.Banner()
    banner_entry.banner_name = xr_infra_cfg.Banner.motd
    banner_entry.banner_text = '#\nTesting your reflex\n#'
    banners.banner.append(banner_entry)

    result = crud.create(provider, banners)

    return 'Banner create result: {}'.format(result)
