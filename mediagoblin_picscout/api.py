# MediaGoblin plugin for searching image metadata in the PicScout database.
#
# Copyright 2013 Commons Machinery http://commonsmachinery.se/
#
# Authors: Artem Popov <artfwo@commonsmachinery.se>
#
# Distributed under GNU Affero GPL v3, please see LICENSE in the top dir.

import json, urllib, urllib2
import requests
import time

from werkzeug.wrappers import Response
from mediagoblin import mg_globals as mgg 
from mediagoblin.db.models import MediaEntry

plugin_config = mgg.global_config['plugins']['mediagoblin_picscout']

# picscout api responses under various conditions
#
# success (cached) {u'ids': [u'...']}
# success (non-cached) {u'timeToQuery': 59, u'followUpUri': u'https://api.picscout.com/v1/search?key=...&url=...'}
# image not found: {u'ids': []}
# wrong key: {u'errorDetails': {u'errorCode': 0, u'description': u'Not Authorized'}}
# wrong id: {u'errorDetails': {u'errorCode': 0, u'description': u'Invalid image id'}}
# bogus fields in /images/: {}

def picscout_lookup(request):
    """
    Try PicScout search for an image, specified in the 'image_url' parameter.
    """

    api_key = plugin_config['api_key']
    
    # load the thumb or medium
    media = MediaEntry.query.filter_by(id=int(request.args['media_id']), state=u'processed').first()
    search_entry = media.media_files.get(plugin_config['search_by'])
    search_file = mgg.public_store.get_local_path(search_entry)

    search_url = 'https://api.picscout.com/v1/search?key=' + api_key
    r = requests.post(search_url, files={"file": open(search_file, 'rb')})
    response_data = r.json()

    if r.status_code != 200:
        details = {'errorDetails': response_data.get('errorDetails', {u'errorCode': 0, u'description': u'Unknown error'})}
        return Response(json.dumps(details), status=r.status_code)

    if response_data.has_key('ids'):
        # sometimes picscout returns ids immediately, so check
        # that id search succeeded and there's a (cached) result
        pass
    else:
        # or wait until picscout is done
        sleep_time = (float(response_data['timeToQuery']) + 1) / 1000
        new_uri = response_data['followUpUri']
        time.sleep(sleep_time)
        r = requests.get(new_uri)
        response_data = r.json()
        if not response_data.has_key('ids'):
            details = {'errorDetails': response_data.get('errorDetails', {u'errorCode': 0, u'description': u'Unknown error'})}
            return Response(json.dumps(details), status=500)

    # we should have at least an empty list of ids now
    ids = []

    for id in response_data['ids']:
        url = "https://api.picscout.com/v1/images/" + id
        r = requests.get(url, params={'key': api_key})
        response_data = r.json()
        print response_data
        if r.status_code != 200:
            details = {'errorDetails': response_data.get('errorDetails', {u'errorCode': 0, u'description': u'Unknown error'})}
            return Response(json.dumps(details), status=r.status_code)
        ids.append(response_data)

    if len(ids) > 0:
        return Response(json.dumps(ids[0]))
    else:
        return Response(json.dumps({}))
