# MediaGoblin plugin for searching image metadata in the PicScout database.
#
# Copyright 2013 Commons Machinery http://commonsmachinery.se/
#
# Authors: Artem Popov <artfwo@commonsmachinery.se>
#
# Distributed under GNU Affero GPL v3, please see LICENSE in the top dir.


import os
import logging

from mediagoblin import mg_globals as mgg
from mediagoblin.tools import pluginapi
from mediagoblin.tools.staticdirect import PluginStatic
from pkg_resources import resource_filename


_log = logging.getLogger(__name__)

PLUGIN_DIR = os.path.dirname(__file__)


def setup_plugin():
    config = pluginapi.get_config('mediagoblin_picscout')

    pluginapi.register_template_path(os.path.join(PLUGIN_DIR, 'templates'))
    pluginapi.register_template_hooks(
        {"image_sideinfo": "mediagoblin/plugins/picscout/sideinfo.html"})

    routes = [
        ('mediagoblin_picscout.api',
         '/api/picscout/picscout_lookup',
         'mediagoblin_picscout.api:picscout_lookup')
    ]

    pluginapi.register_routes(routes)

hooks = {
    'setup': setup_plugin,
    'static_setup': lambda: PluginStatic(
        'mediagoblin_picscout',
        resource_filename('mediagoblin_picscout', 'static'))
}
