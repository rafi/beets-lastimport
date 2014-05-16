# lastimport
Plugin for [beets](http://beets.radbox.org/) that imports Last.fm play counts into database.

## Setup
Clone somewhere and configure beets:

```
pluginpath:
  - /usr/lib/python2.7/site-packages/beetsplug
  - /home/rafi/code/python/beetsplug
plugins: lastimport
lastimport:
  user: rafib
  api_key: secret
```

Get your own [API key](http://www.last.fm/api/account/create) from Last.fm and don't forgot to change the user name in beets configuration.

## Running
To see more information, run with verbose mode:

```
$ beet -v lastimport
...
lastimport: processing: Justice - D.A.N.C.E. (Cross)
lastimport: no match for mb_trackid 12efce96-fef9-4050-86e4-94fbaf8afe90, trying by artist/title/album
lastimport: no album match, trying by artist/title
lastimport: MATCH: Justice - D.A.N.C.E. (Access All Arenas : Live, July 19th 2012: Les Arènes de Nîmes)
lastimport: updating: play_count 118 => 118
lastimport: processing: Justice - DVNO (Cross)
lastimport: MATCH: Justice - DVNO (A Cross the Universe)
lastimport: updating: play_count 99 => 99
...
... updated.
```

## Known Issues
- Need to implement a better fuzzy search, problems with quotes and other non-alphanumerics
- Would like to set live albums with lower precedence

## License
Copyright (c) 2014 Rafael Bodill
The MIT License
