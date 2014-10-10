# Last.fm Play-count Import
Plugin for [beets] that imports your Last.fm library play counts
into beets' database. You can later create [smartplaylists] by querying
`play_count` and do other fun stuff with this field.

To keep up-to-date, you can run this plugin every once in a while (cron?) or use
[mpdstats] to update statistics while listening with [MPD]. By using mpdstats,
you also gain extra fun fields: `rating`, `skip_count`, and `last_played`.

## Dependencies
- [requests] library

## Setup
Clone somewhere and configure beets:

```yml
pluginpath:
  - /usr/lib/python2.7/site-packages/beetsplug
  - /home/rafi/code/python/beetsplug
plugins: lastimport
lastimport:
  per_page: 500
  retry_limit: 3
lastfm:
  user: yourname
  api_key: secret
types:
  play_count: int
  rating: float
```

Get your own [API key] from Last.fm and
don't forgot to change the user name in beets configuration.

## Usages
### Import Play-counts
Simply run `beet lastimport` and wait for the plugin to request tracks from
last.fm and try to match them to beets' database. You will be notified of false
matches, for example:
```
$ beet lastimport

lastimport: Fetching last.fm library for @rafib
lastimport: Querying page #1...
lastimport: Querying page #2/55...
lastimport: Querying page #3/55...
lastimport: Received 500 tracks in this page, processing...
lastimport:   - No match: The Beatles - Maxwell's Silver Hammer (Abbey Road)
lastimport:   - No match: The Beatles - I'm Looking Through You (Rubber Soul)
lastimport: Acquired 480/500 play-counts (20 unknown)
lastimport: Querying page #4/55...
lastimport: Querying page #5/55...
[...]
lastimport: Querying page #53/55...
lastimport: ERROR: unable to read page #53
lastimport: Retrying page #53... (1/3 retry)
lastimport: Retrying page #53... (2/3 retry)
lastimport: Querying page #54/55...
lastimport: Querying page #55/55...
lastimport: ... done!
lastimport: finished processing 55 song pages
lastimport: 935 unknown play-counts
lastimport: 26,565 play-counts imported
```

To see more information, run with verbose mode:
```
$ beet -v lastimport
...
lastimport: match: jj - From Africa to Málaga (jj n° 2) updating: play_count 0 => 61
lastimport: match: Röyksopp - Eple (Melody A.M.) updating: play_count 0 => 60
...
```

#### Song Matching
The plugin fetches your music library from last.fm, then in-order to update
beets it tries to match:
- Musicbrainz track-id
- Artist, title, album
- Artist, title

**Known Issues**:
- Need to implement a better fuzzy search, problems with quotes and other non-alphanumerics
- Would like to set live albums as lower precedence

### Beets Queries
Don't forget to set your `types` plugin with proper data-types.
```bash
beet ls play_count:30..60
beet ls play_count:..10 -f '$artist - $title ($play_count / $rating)'
beet ls rating:0.8..
```
Use the [play] plugin to add songs to your media-player:
```bash
beet play rating:0.7..
```

### Automatic Playlists
You can use the [smartplaylists] plugin to generate automatic playlists with the
`play_count` field.

### Manual Playlists
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
Copyright © 2014 Rafael Bodill

The MIT License

[beets]: http://beets.radbox.org/
[MPD]: http://www.musicpd.org/
[API key]: http://www.last.fm/api/account/create
[requests]: http://docs.python-requests.org/
[smartplaylists]: http://beets.readthedocs.org/en/latest/plugins/smartplaylist.html
[play]: http://beets.readthedocs.org/en/latest/plugins/play.html
[mpdstats]: http://beets.readthedocs.org/en/latest/plugins/mpdstats.html
