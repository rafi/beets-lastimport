# coding=utf-8
# Copyright 2014, Rafael Bodill http://github.com/rafi
#  vim: set ts=8 sw=4 tw=80 et :

import logging
import requests
from beets.plugins import BeetsPlugin
from beets import ui
from beets import dbcore
from beets import config

log = logging.getLogger('beets')
api_url = 'http://ws.audioscrobbler.com/2.0/?method=library.gettracks&user=%s&api_key=%s&format=json&page=%s&limit=%s'

class LastImportPlugin(BeetsPlugin):
    def __init__(self):
        super(LastImportPlugin, self).__init__()
        self.config.add({
            'user':     '',
            'api_key':  '',
            'per_page': 500,
        })

    def commands(self):
        cmd = ui.Subcommand('lastimport',
                        help='import last.fm play counts')

        def func(lib, opts, args):
            import_lastfm(lib)

        cmd.func = func
        return [cmd]

def import_lastfm(lib):
    user = config['lastimport']['user']
    api_key = config['lastimport']['api_key']
    per_page = config['lastimport']['per_page']

    if not user:
        raise ui.UserError('You must specify a user name for lastimport')
    if not api_key:
        raise ui.UserError('You must specify an api_key for lastimport')

    page = get_tracks(user, api_key, 1, per_page)
    if not 'tracks' in page:
        log.error(page)
        raise ui.UserError('Unable to query last.fm')

    total_pages = int(page['tracks']['@attr']['totalPages'])
    if total_pages < 1:
        raise ui.UserError('No data to process, empty query from last.fm')

    for page_num in xrange(1, total_pages):
        page = get_tracks(user, api_key, page_num, per_page)
        if 'tracks' in page:
            process_tracks(lib, page['tracks']['track'])
        else:
            log.info('page {0} has no tracks'.format(page_num))

    log.info('finished processing {0} pages'.format(total_pages))

def get_tracks(user, api_key, page, limit):
    return requests.get(api_url % (user, api_key, page, limit)).json()

def process_tracks(lib, tracks):
    for num in xrange(0, len(tracks)):
        song    = ''
        trackid = tracks[num]['mbid']
        artist  = tracks[num]['artist'].get('name', '')
        title   = tracks[num]['name']
        album   = ''
        if 'album' in tracks[num]:
            album = tracks[num]['album'].get('name', '')

        log.debug(u'lastimport: query: {0} - {1} ({2})'
                .format(artist, title, album))

        # First try to query by musicbrainz's trackid
        if (trackid):
            song = lib.items('mb_trackid:'+trackid).get()

        # Otherwise try artist/title/album
        if (not song):
            #log.debug(u'lastimport: no match for mb_trackid {0}, trying by '
            #        'artist/title/album'.format(trackid))
            query = dbcore.AndQuery([
                dbcore.query.SubstringQuery('artist', artist),
                dbcore.query.SubstringQuery('title', title),
                dbcore.query.SubstringQuery('album', album)
            ])
            song = lib.items(query).get()

        # Last resort, try just artist/title
        if (not song):
            #log.debug(u'lastimport: no album match, trying by artist/title')
            query = dbcore.AndQuery([
                dbcore.query.SubstringQuery('artist', artist),
                dbcore.query.SubstringQuery('title', title)
            ])
            song = lib.items(query).get()

        if (song):
            count = int(song.get('play_count', 0))
            new_count = int(tracks[num]['playcount'])
            log.debug(u'lastimport: match: {0} - {1} ({2})'
                    .format(song.artist, song.title, song.album))
            #log.debug(u'lastimport: updating: play_count {0} => {1}'
            #        .format(count, new_count))
            song['play_count'] = new_count
            song.store()
        else:
            log.info(u'lastimport: NO MATCH: {0} - {1} ({2})'
                    .format(artist, title, album))
