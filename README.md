mg-picscout
===========

This plugin provides a simple backend/ui for searching image metadata
in the PicScout database.

Installation
------------

Download and install mediagoblin_picscout:

    pip install https://github.com/commonsmachinery/mg-picscout/tarball/master

Add the plugin to your mediagoblin_local.ini:

    [[mediagoblin_picscout]]
    api_key=<key provided by PicScout>

Run `./bin/gmg assetlink` to create symlink for plugin resource directory.
