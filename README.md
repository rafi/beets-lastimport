# Last.fm Play-count Import
Plugin for [beets] that imports Last.fm play counts
into the database. You can later create [smartplaylists] by querying
`play_count` and do other fun stuff with this field.
To keep up-to-date, you can run this plugin every once in a while (cron?) or use
[mpdstats] to update statistics while listening with [MPD]. By using mpdstats,
you also gain extra fun fields: `rating`, `skip_count`, and `last_played`.

## Dependency

- [requests] library

## Setup

Clone somewhere and configure beets:

```yml
pluginpath:
  - /usr/lib/python2.7/site-packages/beetsplug
  - /home/rafi/code/python/beetsplug
plugins: lastimport
lastimport:
  user: rafib
  api_key: secret
```

Get your own [API key] from Last.fm and
don't forgot to change the user name in beets configuration.

## Running
Simply run `beet lastimport` and wait for the plugin to request tracks from
last.fm and try to match them to beets' database. You will be notified of false
matches, for example:
```
$ beet lastimport
...
lastimport: NO MATCH: The Beatles - Maxwell's Silver Hammer (Abbey Road)
lastimport: NO MATCH: The Beatles - I'm Looking Through You (Rubber Soul)
lastimport: NO MATCH: Yo La Tengo - If It's True (Popular Songs)
...
```

To see more information, run with verbose mode:
```
$ beet -v lastimport
...
lastimport: query: Amy Winehouse - Wake Up Alone (Back to Black)
lastimport: match: Amy Winehouse - Wake Up Alone (Back to Black)
lastimport: query: Air - La femme d'argent (Moon Safari)
lastimport: match: Air - La Femme d'argent (Moon Safari)
...
```

## Querying
Plugin queries last.fm pages of tracks. It first tries to match by musicbrainz
track-id, then by artist+title+album, and finally by artist+title.

## Known Issues
- Need to implement a better fuzzy search, problems with quotes and other non-alphanumerics
- Would like to set live albums with lower precedence

## Manual Playlists
You can manually create some playlists:
```sh
#!/bin/sh

db_file="$XDG_CACHE_HOME/beets/musiclibrary.blb"
pl_dir="/mnt/media/music/_Playlists"

function query_range() {
	echo "select i.path from item_attributes as a inner
join items as i on (a.entity_id = i.id) where cast(a.value as integer) between
$1 and $2 and a.key = 'play_count'"
}

function query_above() {
	echo "select i.path from item_attributes as a inner
join items as i on (a.entity_id = i.id) where cast(a.value as integer) > $1
and a.key = 'play_count'"
}

sqlite3 $db_file "$(query_range 5 19)" > $pl_dir/listens_low.m3u
sqlite3 $db_file "$(query_range 20 29)" > $pl_dir/listens_20.m3u
sqlite3 $db_file "$(query_range 30 39)" > $pl_dir/listens_30.m3u
sqlite3 $db_file "$(query_range 40 49)" > $pl_dir/listens_40.m3u
sqlite3 $db_file "$(query_above 50)" > $pl_dir/listens_top.m3u
```
Have fun!

## License
Copyright (c) 2014 Rafael Bodill

The MIT License

[beets]: http://beets.radbox.org/
[MPD]: http://www.musicpd.org/
[API key]: http://www.last.fm/api/account/create
[requests]: http://docs.python-requests.org/
[smartplaylists]: http://beets.readthedocs.org/en/latest/plugins/smartplaylist.html
[mpdstats]: http://beets.readthedocs.org/en/latest/plugins/mpdstats.html
