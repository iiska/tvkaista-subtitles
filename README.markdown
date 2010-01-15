TV-kaista subtitles downloader
==============================

Skripti tekstitysten lataamiseen [TVkaistan](http://tvkaista.fi) RSS
-feedeistä [Mirolla](http://getmiro.com) ladatuille YLEn
tekstitetyille ohjelmille. Skripti selvittää gconfin avulla Miron
lataushakemiston ja käy sen sisällön läpi ladaten löytyneille
ohjelmille tekstitykset. Tämän jälkeen skripti jatkaa hakemiston
seurantaa ja lataa automaattisesti uusille sinne ilmestyville
ohjelmille tekstitykset. TVkaistan tunnukset tallentuvat Gnome
keyringiin.


Recursively looks around [Miro's](http://getmiro.com) downloads
directory for [YLE](http://www.yle.fi) programmes which are downloaded
from [TVkaista](http://tvkaista.fi) and tries to download *.srt
subtitles for them. Inotify is used to watch changes in the directory
and new subtitles are downloaded automatically when new video files
are created or moved in.

Dependencies
------------

* Gnome
* python-gconf
* pyinotify

Features
--------

* Login and password for TVkaista are stored in Gnome keyring
* Watches changes in Miro directory and downloads subtitles automatically for new videos
